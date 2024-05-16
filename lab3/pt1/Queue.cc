#ifndef QUEUE
#define QUEUE

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Queue: public cSimpleModule {
private:
    cQueue buffer;
    
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    //Stats para queue
    int dropped;
    int actualCapacity;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
    
    void enqueue(cMessage *msg);
    
public:
    Queue();
    virtual ~Queue();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);

Queue::Queue() {
    endServiceEvent = NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    dropped = 0;
    actualCapacity = par("bufferSize").intValue();
    buffer.setName("buffer");
    bufferSizeVector.setName("Buffer size");
    packetDropVector.setName("Packet Drop");
    endServiceEvent = new cMessage("endService");
    
}

void Queue::finish() {
}

void:: Queue::enqueue(cMessage *msg){
    if (buffer.getLength() >= par("bufferSize").intValue()) {
        //drop the packet
        delete msg;
        this->bubble("Packet deleted");
        dropped++;
        packetDropVector.record(dropped);
    } else {
        //enqueue the packet
        buffer.insert(msg);
        bufferSizeVector.record(buffer.getLength());
        //If the server is idle
        if (!endServiceEvent->isScheduled()){
            //Start the service now
            scheduleAt(simTime()+0, endServiceEvent);
        }
     }
}


void Queue::handleMessage(cMessage *msg) {

    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // dequeue packet
            cPacket *pkt = (cPacket *) buffer.pop();
            // send packet
            send(pkt, "out");
            serviceTime = pkt->getDuration();
            // start new service
            //serviceTime = par("serviceTime");
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    } else {
        // if msg is a data packet, enqueue the packet
        if (buffer.getLength() >= par("bufferSize").intValue()) {
            // Si la cola esta llena, elimina el paquete
            delete msg;
            this->bubble("Packet dropped");
            dropped++;
            packetDropVector.record(dropped);
        } else {
            // Si la cola no esta llena, encola el paquete y si el servidor esta inactivo, comienza el servicio
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());
            if (!endServiceEvent->isScheduled()) {
                scheduleAt(simTime() + 0, endServiceEvent);
            }
        }
    }
}

#endif /* QUEUE */
