#include <iostream>

using namespace std;

class Node{
    public:
    int value = -1;
    Node *next = nullptr;
};

int Access(Node *header, int index);
int Search(Node *header, int value);
void Append(Node *header, int value);
void Insert(Node *header, int index, int value);
void Delete(Node *header, Node *tail, int index);
void PrintList(Node *header);

int main(){
    Node header = Node();
    Node tail = Node();
    header.next = &tail;

    int option = -1;
    int idx = -1;
    int value = -1;
    while(true){
        cout<< "********************************" <<endl;
        PrintList(&header);
        cout<< "1. Append" <<endl;
        cout<< "2. Insert" <<endl;
        cout<< "3. Delete" <<endl;
        cout<< "4. Search" <<endl;
        cout<< "5. Exit" <<endl;
        cout<< "********************************" <<endl;
        cout<< "ToDo: ";
        cin.clear();
        cin >> option;

        switch(option){
            case 1:
            cout<< "\nAppend" << endl;
            cout<< "Value: ";
            cin.clear();
            cin >> value;
            Append(&header, value);
            break;
            case 2:
            cout<< "\nInsert" << endl;
            cout<< "Idx: ";
            cin.clear();
            cin >> idx;
            cout<< "Value: ";
            cin.clear();
            cin >> value;
            Insert(&header, idx, value);
            break;
            case 3:
            cout<< "\nDelete" << endl;
            cout<< "Idx: ";
            cin.clear();
            cin >> idx;
            Delete(&header, &tail, idx);
            break;
            case 4:
            cout<< "\nSearch" << endl;
            cout<< "Value: ";
            cin.clear();
            cin >> value;
            cout<< "Idx: " << Search(&header, value) << endl;
            break;
            case 5:
            return 0;
        }

    }
    return 0;
}

void PrintList(Node *header){
    cout<< "[";
    Node *curNode = header->next;
    while(curNode->next != nullptr){
        cout << " " << curNode->value << " ";
        curNode = curNode->next;
    }

    cout << "]" << endl;
}

int Access(Node *header, int index){
    Node *curNode = header;
    for(int i = 0; i < index + 1; i++){
        // 현재 노드가 tail이 아닐 경우, 다음 노드로 이동
        if(curNode->next != nullptr)
            curNode = curNode->next;
        // tail일 경우 -1 반환
        else
            return -1;
    }
    return curNode->value;
}

int Search(Node *header, int value){
    Node *curNode = header->next;
    int idx = 0;
    while(curNode->next != nullptr){
        if(curNode->value == value)
            return idx;
        idx++;
        curNode = curNode->next;
    }
    return -1;
}

void Append(Node *header, int value){
    Node *curNode = header->next;
    Node *prevNode = header;

    while(curNode->next != nullptr)
    {
        prevNode = curNode;
        curNode = curNode->next;
    }

    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->value = value;
    newNode->next = curNode;
    prevNode->next = newNode;
}

void Insert(Node *header, int index, int value){
    Node *curNode = header->next;
    Node *prevNode = header;

    for(int i = 0; i < index; i++){
        if(curNode->next == nullptr)
            break;
        prevNode = curNode;
        curNode = curNode->next;
    }

    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->value = value;
    newNode->next = curNode;
    prevNode->next = newNode;    
}

void Delete(Node *header, Node *tail, int index){
    Node *curNode = header->next;
    Node *prevNode = header;
    
    for(int i = 0; i < index; i++){
        if(curNode->next == nullptr)
            break;
        prevNode = curNode;
        curNode = curNode->next;
    }

    prevNode->next = curNode->next;
    free(curNode);
}