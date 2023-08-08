#include "iostream"
#include <vector>
#include <map>

using namespace std;

// 괄호는 항상 마지막에 열린 괄호에 대응되는 놈으로 닫혀야 된다는 원리를 이용

int main(){
    vector<char> v;

    // 딕셔너리의 cpp 버전
    map<char, char> dir;

    dir['}'] = '{';
    dir[']'] = '[';
    dir[')'] = '(';
    dir['{'] = '}';
    dir['['] = ']';
    dir['('] = ')';

    char *test_statement = "{[]()}[(({})){}{{}}]\n";
    char *curChar = test_statement;
    char idx = 0;

    cout << "test_statement: ";
    while(*curChar != '\n'){
        cout << *curChar;
        curChar++;
    }
    cout << endl;
    curChar = test_statement;
    while(*curChar != '\n'){
        curChar = test_statement + idx;
        switch(*curChar){
            case '{':
            case '[':
            case '(':
                v.push_back(*curChar);
            break;
            case '}':
            case ']':
            case ')':
                if(dir[*curChar] == v.back()){
                    v.pop_back();
                }
                else{
                    cout << "This statement is invalid" << endl;
                    cout << "idx: " << (int)idx << " / " << "value: " << *curChar <<" must needs to be " << dir[v.back()] << endl;
                    return 0;
                }
            break;

        }
        idx++;
    }
    cout << "This statement is valid" << endl;
}