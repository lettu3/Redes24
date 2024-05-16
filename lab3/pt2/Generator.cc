#ifndef GENERATOR
#define GENERATOR

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Generator : public cSimpleModule {
private:
    cMessage *sendMsgEvent;
    cStdDev transmissionStats;
    int packetsSent;
    //La stat enviados para el send.
    cOutVector packetsSentVector;
    void pktSend();
public:
    Generator();
    virtual ~Generator();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};
Define_Module(Generator);

Generator::Generator() {
    sendMsgEvent = NULL;

}

Generator::~Generator() {
    cancelAndDelete(sendMsgEvent);
}

void Generator::initialize() {
    packetsSentVector.setName("Sent packets: ");
    packetsSent = 0;
    transmissionStats.setName("TotalTransmissions");
    // create the send packet
    sendMsgEvent = new cMessage("sendEvent");
    // schedule the first event at random time
    scheduleAt(par("generationInterval"), sendMsgEvent);
}

void Generator::pktSend() {
    cPacket *pkt = new cPacket("packet");
    pkt->setByteLength(par("packetByteSize"));
    send(pkt,"out");
}

void Generator::finish() {
    recordScalar("Sended packages: ", packetsSent);
}

void Generator::handleMessage(cMessage *msg) {

    pktSend();
    packetsSent++;
    packetsSentVector.record(packetsSent);
    simtime_t departureTime = simTime() + par("generationInterval");
    // schedule the new packet generation
    scheduleAt(departureTime, sendMsgEvent);
}

#endif /* GENERATOR */
