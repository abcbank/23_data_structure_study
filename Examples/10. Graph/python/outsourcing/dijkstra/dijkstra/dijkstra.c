
#include "pch.h"

// resultType: 리턴할 데이터
float resultType[MAX_VERTICES * 2];
// pathGraph: 각 노드의 부모 노드를 저장
int pathGraph[MAX_VERTICES];

// 다익스트라 알고리즘 수행
float* dijkstra(float* graph, int LineLength, int StartNode, int DestNode) {
    // 전달받은 데이터를 기반으로 그래프 데이터 생성
    GraphType g = {
        LineLength,
        graph
    };
    // 연산 수행
    return shortest_path(&g, StartNode, DestNode);
}
// 최소 거리 노드 탐색
int choose(int distance[], int n, int found[])
{
    //각 노드를 나타내는 변수를 설정
    int i, min, minpos;

    //min에 INT_MAX(무한대와 유사, 간선이 연결되지 않은 경우)를 삽입
    min = INT_MAX;
    minpos = -1;
    //최소값 min을 탐색
    for (i = 0; i < n; i++) {
        //방문한 적 없는 노드들에 대해 distance 배열의 값을 비교
        //만약 현재 방문하지 않는 노드 중 i로까지의 거리가 현재 최소값 min보다 작다면,
        if (distance[i] < min && !found[i]) {
            //최소 거리인 i로까지의 거리를 min으로 설정
            min = distance[i];
            //최소값을 가진 노드의 인덱스 i를 minpos에 저장
            minpos = i;
        }
    }
    //최소 거리 노드 인덱스인 i를 반환
    return minpos;
}
//그래프에서 start노드부터의 최단 경로를 탐색
float* shortest_path(GraphType* g, int start, int dest)
{
    int i, u, w;
    // 최단 경로의 가중치 저장
    float* distance = &resultType[0];
    // 각 노드의 이전 노드 저장
    int* path = pathGraph;
    //방문한 정점을 표시
    int found[MAX_VERTICES];
    // 초기화 작업
    for (i = 0; i < g->n; i++)
    {
        //시작 정점 start를 기준으로 했을때 가중치로 distance 배열을 초기화
        distance[i] = g->weight[start * g->n + i];
        //시작 전이므로 방문 여부를 False로 지정
        found[i] = FALSE;
        // 시작 노드와 직접 연결된 노드들의 이전 노드를 시작 노드로 설정
        if (distance[i] < INF)
            path[i] = start;
    }
    // 시작 부분 방문 표시 및 distance 설정
    found[start] = TRUE;
    path[start] = INF;
    distance[start] = 0;
    //시작 정점을 제외한 나머지 정점에 대해 반복
    for (i = 0; i < g->n - 1; i++) {
        //최소값의 인덱스를 u로 지정
        u = choose(distance, g->n, found);
        //현재 distance배열에서 최소값 인덱스인 u를 정점으로 선택
        //인덱스u를 방문 표시
        found[u] = TRUE;
        //가중치가 가장 적은 값을 가진 정점을 집합S에 추가한 뒤 계속하여 새롭게 발견되는 최소 가중치 정보를 수정
        for (w = 0; w < g->n; w++)
            //아직 선택되지 않은 정점 w
            if (!found[w])
                if (distance[u] + g->weight[u * g->n + w] < distance[w]) {
                    distance[w] = distance[u] + g->weight[u * g->n + w];
                    // 갱신 과정에서 w의 이전 노드를 같이 변경
                    path[w] = u;
                }
        //만약 u까지의 최단 거리와 u에서 w의 거리를 합친 거리가 기존의 기준점에서 w까지의 거리보다 가깝다면 그 값으로 정보를 수정
    }
    getShortestRoute(start, dest);
    return resultType;
}

    // 저장된 이전 노드 데이터를 통해 경로 역추적
void getShortestRoute(int start, int dest) {
    float* route = &resultType[MAX_VERTICES];
    int Counter = 0;
    for (int i = 0; i < MAX_VERTICES; i++)
    {
        route[i] = -1.0f;
    }
    // 초기 시작점은 목적지
    int curIdx = dest;
    float temp = 0;

    // 이전 노드가 start일때까지 계속 현재 노드의 부모 노드를 탐색
    while (curIdx != INF && Counter < MAX_VERTICES) {
        route[Counter++] = (float)curIdx;
        curIdx = pathGraph[curIdx];
    }
}