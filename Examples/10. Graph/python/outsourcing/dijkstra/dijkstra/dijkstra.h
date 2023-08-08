#pragma once

#include<stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>
#include <Windows.h>

		
//True�϶� 1�� ����
#define TRUE 1
//False�϶� 0���� ����
#define FALSE 0
//�ִ� ������ ��
#define MAX_VERTICES	120
// ������ ����Ǿ����� �ʴ� ��츦 ���Ѵ�
#define INF	1000000	

typedef struct GraphType {
	// ������ ����
	int n;
	//��Ʈ��ũ�� ���� ����� �ʱ�ȭ
	float* weight;
} GraphType;

__declspec(dllimport) float* dijkstra(float* graph, int LineLength, int StartNode, int DestNode);
int choose(int distance[], int n, int found[]);
float* shortest_path(GraphType* g, int start, int dest);
void getShortestRoute(int start, int dest);