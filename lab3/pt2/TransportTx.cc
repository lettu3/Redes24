//TODO: CAMBIAR TODO A PARADA Y ESPERA
#ifndef TRANSPORT_TX
#define TRANSPORT_TX

#include <omnetpp.h>
#include <string.h>
#include "FeedbackPkt_m.h"
using namespace omnetpp;

class TransportTx: public cSimpleModule {

private:
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    //Estadisticas
    int sent;
    int dropped;
    cOutVector droppedVector;
    cQueue buffer;
    cOutVector bufferSizeVector;
    cQueue bufferFeedback;
    bool sendNext;
public:
    TransportTx();
    virtual ~TransportTx();
protected:
    //bool ackArrived;
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    void sendPacket();
    void enqueueMessage(cMessage *msg); //Common message.
};

Define_Module(TransportTx);

TransportTx::TransportTx(){
    endServiceEvent = NULL;
}

TransportTx::~TransportTx(){
    cancelAndDelete(endServiceEvent);
}

void TransportTx::initialize(){
    dropped = 0;
    sent = 0;
    sendNext = true;
    endServiceEvent = new cMessage("endService");
    droppedVector.setName("Packets Dropped");
    bufferSizeVector.setName("Buffer Size");
    bufferFeedback.setName("Buffer Feedback");
    buffer.setName("Buffer Tx");
}

void TransportTx::finish(){
   // cancelAndDelete(endServiceEvent);
}

void TransportTx::sendPacket() { 
        cPacket *packet = (cPacket *) buffer.pop();
        send(packet, "toOut$o");
        sent++;
        sendNext = false;
        serviceTime = packet->getDuration();
}

void TransportTx::handleMessage(cMessage* msg) {
    if (sendNext && !buffer.isEmpty()) {
        sendPacket();
    }
    else if (msg->getKind() == 0) {
        buffer.insert(msg);
    }
    else if (msg->getKind() == 2) {
        sendNext = true;
        delete msg;
    }
    //TODO hacer records-stats
}


#endif /*TranportTx*/
