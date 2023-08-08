#include "iostream"
#include <vector>
#include <algorithm>
#include <math.h>

using namespace std;

void printHeap(vector<int> v);

int main(){
    vector<int> v;
    int option = -1;
    int value = -1;
    while(true){
        cout<< "********************************" <<endl;
        printHeap(v);
        cout<< "1. push" <<endl;
        cout<< "2. pop" <<endl;
        cout<< "3. Exit" <<endl;
        cout<< "********************************" <<endl;
        cout<< "ToDo: ";
        cin.clear();
        cin >> option;

        switch(option){
            case 1:
            cout<< "\npush" << endl;
            cout<< "Value: ";
            cin.clear();
            cin >> value;
            v.push_back(value);
            push_heap(v.begin(), v.end());
            break;
            case 2:
            cout<< "\npop" << endl;
            pop_heap(v.begin(), v.end());
            cout<< "Value: " << v[0] << endl;
            v.pop_back();
            break;
            case 3:
            return 0;
        }

    } 
}

void printHeap(vector<int> v){
    auto idx = 0;
    auto max_level = log2(v.end() - v.begin());

    for(int i = 0; i <= max_level; i++){
        cout << "Level " << (i) << ":";
        for(int j = 0; j < pow(2, i) & (pow(2, i) + j) <= (v.end() - v.begin()); j++){
            cout << " " << v[idx];
            idx++;
        }
        cout<<endl;
    }
}