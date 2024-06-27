#ifndef APP
#define APP

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class App: public cSimpleModule {
private:
    cMessage *sendMsgEvent;
    cStdDev delayStats;
    cOutVector delayVector;
    simtime_t avgDelay;
    int sentPackets;
    int receivedPackets;
    int lostPackets;
    cOutVector avgDelayVector;
    cOutVector sentPacketsVector;
    cOutVector receivedPacketsVector;
    cOutVector lostPacketsVector;

public:
    App();
    virtual ~App();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(App);

#endif /* APP */

App::App() {
}

App::~App() {
}

void App::initialize() {

    // If interArrivalTime for this node is higher than 0
    // initialize packet generator by scheduling sendMsgEvent
    if (par("interArrivalTime").doubleValue() != 0) {
        sendMsgEvent = new cMessage("sendEvent");
        scheduleAt(par("interArrivalTime"), sendMsgEvent);
    }

    sentPackets = 0;
    receivedPackets = 0;
    lostPackets = 0;
    avgDelay = 0;
    // Initialize statistics
    delayVector.setName("Delay");
    sentPacketsVector.setName("SentPackets");
    receivedPacketsVector.setName("ReceivedPackets");
    lostPacketsVector.setName("LostPackets");

}

void App::finish() {
    // Record statistics
    //recordScalar("Average delay", delayStats.getMean());
    /*
    recordScalar("Number of packets", delayStats.getCount());
    recordScalar("Number of lost packets", lostPackets);
    recordScalar("Number of received packets", receivedPackets);
    recordScalar("Number of sent packets", sentPackets);
    recordScalar("Packet loss rate", lostPackets / sentPackets);
    recordScalar("Packet delivery rate", receivedPackets / sentPackets);
    */
}

void App::handleMessage(cMessage *msg) {

    // if msg is a sendMsgEvent, create and send new packet
    if (msg == sendMsgEvent) {
        // create new packet
        Packet *pkt = new Packet("packet",this->getParentModule()->getIndex());
        pkt->setByteLength(par("packetByteSize"));
        pkt->setSource(this->getParentModule()->getIndex());
        pkt->setDestination(par("destination"));

        // send to net layer
        send(pkt, "toNet$o");
        sentPackets++;
        sentPacketsVector.record(sentPackets);

        // compute the new departure time and schedule next sendMsgEvent
        simtime_t departureTime = simTime() + par("interArrivalTime");
        scheduleAt(departureTime, sendMsgEvent);

    }
    // else, msg is a packet from net layer
    else {
        // compute delay and record statistics
        simtime_t delay = simTime() - msg->getCreationTime();
        delayStats.collect(delay);
        delayVector.record(delay);
        //avgDelay += delay;
        receivedPackets++;
        receivedPacketsVector.record(receivedPackets);
        // delete msg
        delete (msg);
    }

}
