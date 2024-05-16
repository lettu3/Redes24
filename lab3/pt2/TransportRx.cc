//TODO:CAMBIAR TODO A PARADA Y ESPERA
#ifndef TRANSPORT_RX
#define TRANSPORT_RX

#include <omnetpp.h>
#include <string.h>
#include "FeedbackPkt_m.h"

using namespace omnetpp;

class TransportRx: public cSimpleModule {

    private:
        cMessage *feedbackEvent;
        cMessage *endServiceEvent;
    //Estadisticas
        int dropped;
        int sent;
        cOutVector droppedVector;
        cOutVector sentVector;
        cQueue buffer;
        cOutVector bufferSizeVector;
        cQueue bufferFeedback;

    public:
        TransportRx();
        virtual ~TransportRx();
    protected:
        //bool ackArrived;
        virtual void initialize();
        virtual void finish();
        virtual void handleMessage(cMessage *msg);
        void sendPacket();
        void sendFeedback();
        void enqueueMessage(cMessage *msg); //Common message.
        void enqueueFeedback(cMessage *msg); //feedback
        //void sendACK();
};

Define_Module(TransportRx);

TransportRx::TransportRx(){
    feedbackEvent = NULL;
    endServiceEvent = NULL;
}

void TransportRx::initialize(){
    sent = 0;
    dropped = 0;
    droppedVector.setName("Packets Dropped");
    bufferSizeVector.setName("buffer size");
    bufferFeedback.setName("Buffer Feedback");
    sentVector.setName("Packets sent to Gen");
    buffer.setName("Buffer Rx");
    //Initialize events.
    feedbackEvent = new cMessage("endFeedback");
    endServiceEvent = new cMessage("endService");
}

void TransportRx::finish(){
   //cancelAndDelete(feedbackEvent); //From generator
   // cancelAndDelete(endServiceEvent);
}

void TransportRx::sendPacket() {
    if (!buffer.isEmpty()) {
        this->bubble("Entro al if");
        cPacket *packet = (cPacket *) buffer.pop();
        send(packet, "toApp");
        sent++;
        sentVector.record(sent);
        simtime_t serviceTime = packet->getDuration();
        scheduleAt(simTime() + serviceTime, endServiceEvent);
    }
}

void TransportRx::handleMessage(cMessage *msg) {
    //int bufferMaxLength = par("bufferSize").intValue();
    /*if (buffer.getLength() >= bufferMaxLength) { //Buffer is full
        delete msg;
        dropped++;
        droppedVector.record(dropped);
        this->bubble("Packet dropped");
    } else { //Buffer is not full
        //Como esta en la consigna
        if(msg == endServiceEvent){

        }
        }
        sendFeedback();
    }
    buffer.insert(msg);
    */

    if (msg->getKind() == 2){
      enqueueFeedback(msg);
    } else {
        if (msg == feedbackEvent){
            sendFeedback();
        } else if (msg == endServiceEvent){
            sendPacket();
        } else {
            enqueueMessage(msg);
        }
    }
}

TransportRx::~TransportRx(){
    cancelAndDelete(endServiceEvent);
}


void TransportRx::sendFeedback() {
    this->bubble("feedback");

    if(!bufferFeedback.isEmpty()) {
        FeedbackPkt *feedbackPkt = (FeedbackPkt *) bufferFeedback.pop();
        send(feedbackPkt, "toOut$o");
        scheduleAt(simTime() + feedbackPkt->getDuration(), feedbackEvent);
        this->bubble("feedback sent");

    }
}

void TransportRx::enqueueMessage(cMessage *msg) {
    const int bufferMaxSize = par("bufferSize").intValue();

    if(buffer.getLength() >= bufferMaxSize) {
        delete msg;
        this->bubble("Packet dropped");
        dropped++;
        droppedVector.record(dropped);
    } else {
        FeedbackPkt *feedbackPkt = new FeedbackPkt();
        feedbackPkt->setByteLength(20);
        feedbackPkt->setKind(2);

        //ya podes enviar el siguiente paquete flaco
        feedbackPkt->setSendNextPkt(true);
        enqueueFeedback(feedbackPkt);
        /*
         * cajon 10 manzanas, ocupo 3 --> 10-3/10 = 0.7 es lo que me queda (remainingRatio)
        */

        /*float remainingRatio = (par("bufferSize").intValue() - buffer.getLength())/
                                (float)par("bufferSize").intValue();
        feedbackPkt->setRemainingBuffer(par("bufferSize").intValue() - buffer.getLength());
        feedbackPkt->setRemainingRatio(remainingRatio);
        enqueueFeedback(feedbackPkt);
        */
        recordScalar("Buffer Size", buffer.getLength()); //OJO
        buffer.insert(msg);
        EV << "Valor de miVariable: " << buffer.getLength() << endl;

        if(!endServiceEvent->isScheduled()) {
            scheduleAt(simTime() + 0, endServiceEvent);
        }
    }

}

void TransportRx::enqueueFeedback(cMessage *msg) {
    bufferFeedback.insert(msg);

    if(!feedbackEvent->isScheduled()) {
        scheduleAt(simTime() + 0, feedbackEvent);
    }
}

#endif /*TransportRx*/
