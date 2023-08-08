#pragma once

#include<stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>
#include <Windows.h>

		
//True일때 1로 정의
#define TRUE 1
//False일때 0으로 정의
#define FALSE 0
//최대 정점의 수
#define MAX_VERTICES	120
// 간선이 연결되어있지 않는 경우를 무한대
#define INF	1000000	

typedef struct GraphType {
	// 정점의 개수
	int n;
	//네트워크의 인접 행렬을 초기화
	float* weight;
} GraphType;

__declspec(dllimport) float* dijkstra(float* graph, int LineLength, int StartNode, int DestNode);
int choose(int distance[], int n, int found[]);
float* shortest_path(GraphType* g, int start, int dest);
void getShortestRoute(int start, int dest);