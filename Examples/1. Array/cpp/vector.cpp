#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void printVector(vector<int> v);

int main(){
    vector<int> v;
    int option = -1;
    int index = -1;
    int value = -1;
    while(true){
        cout<< "********************************" <<endl;
        printVector(v);
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
            v.push_back(value);
            break;
            case 2:
            cout<< "\nInsert" << endl;
            cout<< "Index: ";
            cin.clear();
            cin >> index;
            if(v.end() - v.begin() > index){
                cout<< "Value: ";
                cin.clear();
                cin >> value;
                v.insert(v.begin() + index, value);
            }
            break;
            case 3:
            cout<< "\nDelete" << endl;
            cout<< "Index: ";
            cin.clear();
            cin >> index;
            if(v.end() - v.begin() > index){
                v.erase(v.begin() + index);
            }
            break;
            case 4:
            {
                cout<< "\nSearch" << endl;
                cout<< "Value: ";
                cin.clear();
                cin >> value;
                auto valIdx  = std::find(v.begin(), v.end(), value);
                
                if(valIdx != v.end()){
                    cout << "Index of " << value << ": " 
                        << (valIdx - v.begin()) << endl;
                }
                else{
                    cout << "Vector Not Contains " << value << endl;
                }
                break;
            }
            case 5:
            return 0;
        }

    } 
}

void printVector(vector<int> v){
    cout << "[begin]";
    auto t = v.begin();
    auto e = v.end();
    for(auto i = 0; i < v.end() - v.begin(); i++){
        cout << " " << v[i] << " ";
    }

    cout << "[end]" << endl;
}