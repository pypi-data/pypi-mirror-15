import hashlib
import struct
import math
import sys
import os
import time
import getpass
from bitstring import BitArray
import bencode
import requests
from peers import PeerManager
import pieces
import logging
from sys import platform

logging = logging.getLogger('bittorrent')

OKBLUE = '\033[94m'
RESET_SEQ = "\033[0m"

HEADER_SIZE = 28 

def checkValidPeer(peer, infoHash):
    peerInfoHash = peer.bufferRead[HEADER_SIZE:HEADER_SIZE+len(infoHash)]
    
    if peerInfoHash == infoHash:
        peer.bufferRead = peer.bufferRead[HEADER_SIZE+len(infoHash)+20:]
        peer.handshake = True
        logging.debug("Handshake Valid")
        return True
    else:
        return False

def convertBytesToDecimal(headerBytes, power):
    size = 0
    for ch in headerBytes:
        size += int(ord(ch))*256**power
        power -= 1
    return size

def handleHave(peer, payload):
    index = convertBytesToDecimal(payload, 3)
    logging.debug("Handling Have")
    peer.bitField[index] = True

def makeInterestedMessage():
    interested = '\x00\x00\x00\x01\x02'

    return interested

def sendRequest(index, offset, length):
    header = struct.pack('>I', 13)
    id = '\x06'
    index = struct.pack('>I', index)
    offset = struct.pack('>I', offset)
    length = struct.pack('>I', length)
    request = header + id + index + offset + length
    return request

def pipeRequests(peer, peerMngr):
    if len(peer.bufferWrite) > 0:
        return True

    for i in xrange(10):
        nextBlock = peerMngr.findNextBlock(peer)
        if not nextBlock:
            return 

        index, offset, length = nextBlock
        peer.bufferWrite = sendRequest(index, offset, length)
        
def process_message(peer, peerMngr, shared_mem):
    while len(peer.bufferRead) > 3:
        if not peer.handshake:
            if not checkValidPeer(peer, peerMngr.infoHash):
                return False
            elif len(peer.bufferRead) < 4:
                return True

        msgSize = convertBytesToDecimal(peer.bufferRead[0:4], 3)
        if len(peer.bufferRead) == 4:
            if msgSize == '\x00\x00\x00\x00':
                return True
            return True 
        
        msgCode = int(ord(peer.bufferRead[4:5]))
        payload = peer.bufferRead[5:4+msgSize]
        if len(payload) < msgSize-1:
            return True
        peer.bufferRead = peer.bufferRead[msgSize+4:]
        if not msgCode:
            continue
        elif msgCode == 0:
            peer.choked = True
            continue
        elif msgCode == 1:
            logging.debug("Unchoked! Finding block")
            peer.choked = False
            pipeRequests(peer, peerMngr)
        elif msgCode == 4:
            handleHave(peer, payload)
        elif msgCode == 5:
            peer.setBitField(payload)
        elif msgCode == 7:
            index = convertBytesToDecimal(payload[0:4], 3)
            offset = convertBytesToDecimal(payload[4:8], 3)
            data = payload[8:]
            if index != peerMngr.curPiece.pieceIndex:

                return True

            piece = peerMngr.curPiece           
            result = piece.addBlock(offset, data)

            if not result:
                logging.debug("Not successful adding block. Disconnecting.")
                return False
            
            if piece.finished:
                peerMngr.numPiecesSoFar += 1
                if peerMngr.numPiecesSoFar < peerMngr.numPieces:
                    peerMngr.curPiece = peerMngr.pieces.popleft()
                shared_mem.put((piece.pieceIndex, piece.blocks))
                # logging.info(("\rDownloaded piece: %d ") % piece.pieceIndex)
                
            pipeRequests(peer, peerMngr)

        if not peer.sentInterested:
            logging.debug("Bitfield initalized. "
                          "Sending peer we are interested...")
            peer.bufferWrite = makeInterestedMessage()
            peer.sentInterested = True
    return True

def generateMoreData(myBuffer, shared_mem):
    while not shared_mem.empty():
        index, data = shared_mem.get()
        if data:
            myBuffer += ''.join(data)
            yield myBuffer
        else:
            raise ValueError('Pieces was corrupted. Did not download piece properly.')

def writeToMultipleFiles(files, path, peerMngr):
    bufferGenerator = None
    myBuffer = ''
    
    for f in files:
        p = path.join(f['path'])
        if not os.path.exists(os.path.dirname(p)):
            os.makedirs(os.path.dirname(p))
        with open(p, "w") as fileObj:
            length = f['length']
            if not bufferGenerator:
                bufferGenerator = generateMoreData(myBuffer, peerMngr)

            while length > len(myBuffer):
                myBuffer = next(bufferGenerator)

            fileObj.write(myBuffer[:length])
            myBuffer = myBuffer[length:]

def writeToFile(file, length, peerMngr):
    user = getpass.getuser()
    if platform == "win32":
        fileObj = open('C:\Users\%s\Downloads\\' %user + file, 'wb')
    else:
        fileObj = open('/home/%s/Downloads' %user + file, 'wb')
    myBuffer = ''
   
    bufferGenerator = generateMoreData(myBuffer, peerMngr)

    while length > len(myBuffer):
        myBuffer = next(bufferGenerator)

    fileObj.write(myBuffer[:length])
    fileObj.close()

def write(info, peerMngr):
    user = getpass.getuser()
    if 'files' in info:
        if platform == "win32":
            path = 'C:\Users'+'\\'+ user + '\Downloads\\'+ info['name'] + '/'
        else:
            path = '/home/'+ user +'/Downloads/' + info['name'] + '/'
        writeToMultipleFiles(info['files'], path, peerMngr)    
    else:
        writeToFile(info['name'], info['length'], peerMngr)
