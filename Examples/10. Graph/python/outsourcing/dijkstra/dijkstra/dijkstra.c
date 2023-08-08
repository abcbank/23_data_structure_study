
#include "pch.h"

// resultType: ������ ������
float resultType[MAX_VERTICES * 2];
// pathGraph: �� ����� �θ� ��带 ����
int pathGraph[MAX_VERTICES];

// ���ͽ�Ʈ�� �˰��� ����
float* dijkstra(float* graph, int LineLength, int StartNode, int DestNode) {
    // ���޹��� �����͸� ������� �׷��� ������ ����
    GraphType g = {
        LineLength,
        graph
    };
    // ���� ����
    return shortest_path(&g, StartNode, DestNode);
}
// �ּ� �Ÿ� ��� Ž��
int choose(int distance[], int n, int found[])
{
    //�� ��带 ��Ÿ���� ������ ����
    int i, min, minpos;

    //min�� INT_MAX(���Ѵ�� ����, ������ ������� ���� ���)�� ����
    min = INT_MAX;
    minpos = -1;
    //�ּҰ� min�� Ž��
    for (i = 0; i < n; i++) {
        //�湮�� �� ���� ���鿡 ���� distance �迭�� ���� ��
        //���� ���� �湮���� �ʴ� ��� �� i�α����� �Ÿ��� ���� �ּҰ� min���� �۴ٸ�,
        if (distance[i] < min && !found[i]) {
            //�ּ� �Ÿ��� i�α����� �Ÿ��� min���� ����
            min = distance[i];
            //�ּҰ��� ���� ����� �ε��� i�� minpos�� ����
            minpos = i;
        }
    }
    //�ּ� �Ÿ� ��� �ε����� i�� ��ȯ
    return minpos;
}
//�׷������� start�������� �ִ� ��θ� Ž��
float* shortest_path(GraphType* g, int start, int dest)
{
    int i, u, w;
    // �ִ� ����� ����ġ ����
    float* distance = &resultType[0];
    // �� ����� ���� ��� ����
    int* path = pathGraph;
    //�湮�� ������ ǥ��
    int found[MAX_VERTICES];
    // �ʱ�ȭ �۾�
    for (i = 0; i < g->n; i++)
    {
        //���� ���� start�� �������� ������ ����ġ�� distance �迭�� �ʱ�ȭ
        distance[i] = g->weight[start * g->n + i];
        //���� ���̹Ƿ� �湮 ���θ� False�� ����
        found[i] = FALSE;
        // ���� ���� ���� ����� ������ ���� ��带 ���� ���� ����
        if (distance[i] < INF)
            path[i] = start;
    }
    // ���� �κ� �湮 ǥ�� �� distance ����
    found[start] = TRUE;
    path[start] = INF;
    distance[start] = 0;
    //���� ������ ������ ������ ������ ���� �ݺ�
    for (i = 0; i < g->n - 1; i++) {
        //�ּҰ��� �ε����� u�� ����
        u = choose(distance, g->n, found);
        //���� distance�迭���� �ּҰ� �ε����� u�� �������� ����
        //�ε���u�� �湮 ǥ��
        found[u] = TRUE;
        //����ġ�� ���� ���� ���� ���� ������ ����S�� �߰��� �� ����Ͽ� ���Ӱ� �߰ߵǴ� �ּ� ����ġ ������ ����
        for (w = 0; w < g->n; w++)
            //���� ���õ��� ���� ���� w
            if (!found[w])
                if (distance[u] + g->weight[u * g->n + w] < distance[w]) {
                    distance[w] = distance[u] + g->weight[u * g->n + w];
                    // ���� �������� w�� ���� ��带 ���� ����
                    path[w] = u;
                }
        //���� u������ �ִ� �Ÿ��� u���� w�� �Ÿ��� ��ģ �Ÿ��� ������ ���������� w������ �Ÿ����� �����ٸ� �� ������ ������ ����
    }
    getShortestRoute(start, dest);
    return resultType;
}

    // ����� ���� ��� �����͸� ���� ��� ������
void getShortestRoute(int start, int dest) {
    float* route = &resultType[MAX_VERTICES];
    int Counter = 0;
    for (int i = 0; i < MAX_VERTICES; i++)
    {
        route[i] = -1.0f;
    }
    // �ʱ� �������� ������
    int curIdx = dest;
    float temp = 0;

    // ���� ��尡 start�϶����� ��� ���� ����� �θ� ��带 Ž��
    while (curIdx != INF && Counter < MAX_VERTICES) {
        route[Counter++] = (float)curIdx;
        curIdx = pathGraph[curIdx];
    }
}