#include <iostream>

using namespace std;

#define MAX_LEN 20

class Stack{
    public:
    void push(int value);
    int pop();
    int peek();
    bool isEmpty();
    bool isFull();
    void printStack();
    
    private:
    int top = -1;
    int datas[MAX_LEN]; 
};

bool Stack::isEmpty(){
    return this->top == - 1;
}

bool Stack::isFull(){
    return this->top == MAX_LEN - 1;
}

void Stack::push(int value){
    if(!this->isFull())
        this->datas[++top] = value;
    else
        this->datas[top] = value;
}

int Stack::pop(){
    return this->isEmpty() ?  -1 : this->datas[top--];
}

int Stack::peek(){
    return this->top;
}

void Stack::printStack(){
    cout<< "[bottom]";
    for(int i = 0; i <= this->top; i++)
        cout<< " "  << this->datas[i] << " ";
    cout << "[top]" << endl;
}

int main(){
    Stack stack = Stack();      
    int option = -1;
    int value = -1;
    while(true){
        cout<< "********************************" <<endl;
        stack.printStack();
        cout<< "1. Push" <<endl;
        cout<< "2. Pop" <<endl;
        cout<< "3. Peek" <<endl;
        cout<< "4. isEmpty" <<endl;
        cout<< "5. isFull" <<endl;
        cout<< "6. Exit" <<endl;
        cout<< "********************************" <<endl;
        cout<< "ToDo: ";
        cin.clear();
        cin >> option;

        switch(option){
            case 1:
            cout<< "\nPush" << endl;
            cout<< "Value: ";
            cin.clear();
            cin >> value;
            stack.push(value);
            break;
            case 2:
            cout<< "\nPop" << endl;
            cout<< "Value: " << stack.pop()<< endl;
            break;
            case 3:
            cout<< "\nPeek" << endl;
            cout<< "Current Top: " << stack.peek()<< endl;
            break;
            case 4:
            cout<< "\nisEmpty" << endl;
            cout<< "Data: " + stack.peek() << " / " << MAX_LEN << endl;
            cout<< "isEmpty:" << stack.isEmpty() << endl;
            break;
            case 5:
            cout<< "\nisEmpty" << endl;
            cout<< "Data: " + stack.peek() << " / " << MAX_LEN << endl;
            cout<< "isFull:" << stack.isEmpty() << endl;
            break;
            case 6:
            return 0;
        }

    } 
}