#include <iostream>
#include <queue>

using namespace std;

void printQueue(queue<int> q);

// 하중을 50만큼 만큼 견딜 수 있는 다리가 있다. 모든 자동차는 다리를 건너기 위해 3분이라는 시간이 필요하고 자동차는 앞의 자동차가 출발하고 1분 후 다리에 
// 진입할 수 있다. 각 자동차의 무게는 입력으로 주어진다.
// 이때, 입력한 모든 자동차가 다리를 건너기 위해 필요한 시간을 계산해라.

int main(){
    queue<int> q;
    // 최대 세개의 차가 다리에서 달릴 수 있음
    queue<int> onBridge;

    int input[10] = {10, 10, 30, 50, 30, 10, 20, 20, 20};

    int curWeight = 0;
    int MaxWeight = 50;

    int totalTime = -1;

    for(int i = 0; i < 10; i++)
        q.push(input[i]);

    onBridge.push(0);
    onBridge.push(0);
    onBridge.push(0);

    while(!q.empty()){
        // 1회 루프를 1분이라 생각하자

        // 이전 루프에 비해 1분이 지났으므로 onBridge 큐에서 하나를 빼고
        curWeight -= onBridge.front();
        onBridge.pop();

        // 1) 아직 견딜수 있는 하중이 남아있을때
        if(curWeight < MaxWeight){
            // 다음 차의 하중을 확인
            int nextCar = q.front();
            // 다음 차의 하중이 여유있다면
            if(curWeight + nextCar <= MaxWeight){
                // 차를 보냄
                curWeight += nextCar;
                onBridge.push(nextCar);
                q.pop();
            }
            else{
                onBridge.push(0);
            }
        }
        // 2) 하중이 남아있지 않을때
        else{
            // 대기
            onBridge.push(0);
        }

        totalTime += 1;
    }
    // 입력 큐가 완전히 비었을때 = 마지막 차량이 막 도로 위에서 출발했을때
    // 따라서 결과에 3을 더해줌
    cout << "총 소모 시간: " << totalTime + 3 << "분" << endl;

    return 0;

}