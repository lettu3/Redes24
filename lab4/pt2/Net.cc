#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

#define HELLO 0
#define DATA 1
#define MAX_SIZE 20
using namespace omnetpp;

class Net: public cSimpleModule {
private:

public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    void handleHelloPacket(Packet *pkt);
    void handleDataPacket(Packet *pkt);
    void chooseOutput();
    int * actual_network;
    int id;
    int net_size;
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {

    id = getParentModule()->getIndex();
    EV << "Hola, soy " << id << "\n";
    // Creamos un paquete HELLO que mandamos en sentido horario, con source = destination
    // para dar una vuelta completa.

    Packet *hello_pkt = new Packet();
    hello_pkt->setKind(HELLO);
    hello_pkt->setByteLength(20);
    hello_pkt->setSource(id);
    hello_pkt->setDestination(id);
    hello_pkt->setAge(MAX_SIZE);
    hello_pkt->setPos(0);
    send(hello_pkt, "toLnk$o", 0);


}

void Net::finish() {
    free(actual_network);
}

void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;

    // If this node is the final destination, send to App
    if(pkt->getKind() == HELLO){
        handleHelloPacket(pkt);
    }
    else if(pkt->getKind() == DATA) {
        handleDataPacket(pkt);
    }
}

void Net::handleHelloPacket(Packet *pkt) {

    cGate *arrivalGate = pkt->getArrivalGate();

    if(pkt->getAge() == 0){
        // se deja de reenviar
        delete(pkt);
    }
    else if( pkt->getDestination() == id){
        net_size = pkt->getPos()+1;
        pkt->insertTopology(net_size-1, id);
        actual_network = (int*)malloc(sizeof(int) * net_size);
        for(int i = 0; i < net_size; i++){
            // los insert() en topology fueron moviendo los elementos
            // quiero que esté bien --> doy vuelta el arreglo topology
            actual_network[(i+1) % net_size] = pkt->getTopology(i);
        }

        delete(pkt);

    }
    else {
        pkt->setAge(pkt->getAge() - 1);
        int actualPos = pkt->getPos() + 1;
        EV << actualPos;
        pkt->setPos(actualPos);
        pkt->insertTopology(actualPos - 1, id);
        send(pkt, "toLnk$o", 0);

    }
}


void Net::handleDataPacket(Packet *pkt) {
    int dest = pkt->getDestination();
    if (dest == this->getParentModule()->getIndex()) {
        send(pkt, "toApp$o");
    }
    // If not, forward the packet to some else... to who?

    else{
        int out;
        int pos = 0;
        bool founded = false;
        while(!founded){
            if(actual_network[pos] == dest){
                founded = true;
            }
            else {
                pos++;
            }
        }
        bool symmetric = (net_size % 2 == 0) && (net_size/ 2 == pos);

        if(symmetric){
            out = intuniform(0, 1); // se randomiza la salida
            EV << "Symmetric\n";
        }
        else if(pos < net_size / 2 ) {
            out = 0;
        }
        else {
            out = 1;
        }
        send(pkt, "toLnk$o", out);
    }
}




//     else if (pkt->getSource() == this->getParentModule()->getIndex){
