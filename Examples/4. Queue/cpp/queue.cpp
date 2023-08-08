#include <iostream>

using namespace std;

#define MAX_LEN 3

class Queue{
    public:
    void enqueue(int value);
    int dequeue();
    int peek();
    bool isEmpty();
    bool isFull();
    void printQueue();
    
    private:
    int front = 0;
    int rear = 0;
    int datas[MAX_LEN]; 
};

bool Queue::isEmpty(){
    return this->front == this->rear;
}

// MAX_LEN 만큼 데이터를 저장할 경우, isEmpty와 동일하게 front와 rear값이
// 동일하짐. 따라서 큐는 늘 하나가 비워져있는 상태를 full 상태로 간주함.
bool Queue::isFull(){
    return this->front != 0 ? 
            (this->front - 1) == this->rear :
            (MAX_LEN - 1) == this->rear;
}

void Queue::enqueue(int value){
    if(!this->isFull()){
        this->datas[this->rear] = value; 
        this->rear = (this->rear + 1) % MAX_LEN; 
    }
    else
        this->datas[this->rear - 1] = value;
}

int Queue::dequeue(){
    if(this->isEmpty()){
        return -1;
    }
    else{
        int value = this->datas[this->front];
        this->front = (this->front + 1) % MAX_LEN;
        return value;
    }
}

int Queue::peek(){
    return this->front;
}

void Queue::printQueue(){
    cout<< "front idx:" << ((int)this->front)<<endl;
    cout<< "rear idx:" << ((int)this->rear)<<endl;
    cout<< "[front]";
    for(int i = this->front; i < this->rear; i =(i + 1) % MAX_LEN)
        cout<< " "  << this->datas[i] << " ";
    cout << "[rear]" << endl;
}

int main(){
    Queue q = Queue();      
    int option = -1;
    int value = -1;
    while(true){
        cout<< "********************************" <<endl;
        q.printQueue();
        cout<< "1. Enqueue" <<endl;
        cout<< "2. Dequeue" <<endl;
        cout<< "3. Exit" <<endl;
        cout<< "********************************" <<endl;
        cout<< "ToDo: ";
        cin.clear();
        cin >> option;

        switch(option){
            case 1:
            cout<< "\nEnqueue" << endl;
            cout<< "Value: ";
            cin.clear();
            cin >> value;
            q.enqueue(value);
            break;
            case 2:
            cout<< "\nDequeue" << endl;
            cout<< "Value: " << q.dequeue()<< endl;
            break;
            case 3:
            return 0;
        }

    } 
}