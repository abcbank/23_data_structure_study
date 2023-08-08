var map = null;
var JCs = [];
var Highways = [];
var Path = [];
var SelectingSource = false;
var SelectingDestination = false;

var Colors = [
    '#000000',    '#0000ff',    '#00ff00',    '#ff0000',    '#ffff00',    '#ff00ff',    '#00ffff',    '#5a2b84',    '#13aa4f',    '#5368b4',
    '#124fea',    '#dee049',    '#2f7879',    '#20b100',    '#cd4b06',    '#9a67d7',    '#e315d6',    '#bd879f',    '#471b8b',    '#60d478',
    '#96cdc1',    '#b95ba4',    '#35261a',    '#634be8',    '#2829ce',    '#29288b',    '#5fc9bd',    '#9a3287',    '#aeeca4',    '#bc1c9a',
    '#aba742',    '#a1e43f',    '#e70d16',    '#898441',    '#e9cc80',    '#6188ea',    '#f81ca2',    '#e56eea',    '#45060f',    '#d49307',
    '#43af0c',    '#e97e87',    '#ee8cda',    '#a281db',    '#f30597',    '#5be651',    '#455b3f',    '#a79186',    '#f86f5f',    '#8d19fa',    
    '#207ff1',    '#f3eb81'
]
function init(JCarray, Highwayarray, Patharray){
    JCs = [];
    // JCarray에 대해, 각 JC의 이름 및 위경도 추출 후 리스트에 추가
    JCarray.forEach((item) => {
        JCs.push({title: item[0], latlng: new kakao.maps.LatLng(parseFloat(item[4]),parseFloat(item[5]))});
    });
    Highways = [];
    // Highwayarray에 대해, 각 고속도로의 이름 및 JC 연결 상태를 추출 후 리스트에 추가
    Highwayarray.forEach((item) => {
        HighwayJC = []
        extractJC(item[1]).forEach((Name) => {
            HighwayJC.push(JCs.filter(JC => JC.title == Name)[0]);
        })
        Highways.push({title: item[0], JCList: HighwayJC});
    });
    // Patharray에 값이 있을 경우 -> 출발지와 목적지의 경로를 표시해야 함
    if(Patharray.length > 0){
        
        // 경로 데이터셋에서 경로 추출
        Path = []
        extractJC(Patharray[7]).forEach((Name) => {
            Path.push(JCs.filter(JC => JC.title == Name)[0]);
        })

        // 카카오 맵을 표시할 영역 선택
        var mapContainer = document.getElementById('map'), 
        
        // 맵 옵션 설정
        mapOption = { 
            center: new kakao.maps.LatLng(Patharray[5], Patharray[6]), // 지도의 중심좌표
            level: 10 // 지도의 확대 레벨
        };
    
        // 맵 생성
        map = new kakao.maps.Map(mapContainer, mapOption);
        // 경로에 있는 JC들의 마커 생성
        printMarker(Path)
        // 경로를 따라 라인 생성
        printLine(Path)    
        
        // 출발지와 목적지 input 초기화
        document.getElementById("validationDefaultSource").value  = Patharray[0];
        document.getElementById("validationDefaultDestination").value  = Patharray[1];
    }
    // 값이 없을 경우 -> JC와 고속도로 표시해야함
    else{
        var mapContainer = document.getElementById('map'), 
        
        mapOption = { 
            center: new kakao.maps.LatLng(37.541, 126.986), 
            level: 10 
        };

        map = new kakao.maps.Map(mapContainer, mapOption); 
        
        // 모든 JC 표시
        printMarker(JCs)
        // 모든 고속도로 경로 표시
        for(var i = 0; i < Highways.length; i++){
            printLine(Highways[i].JCList, Colors[i])
        }
    }
}

// JC 리스트를 매개변수로 받아 모든 JC리스트에 대해 마커 표시
function printMarker(JCList){
    if(JCList != null){
        // 카카오 기본 마커 이미지 주소
        var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
        for (var i = 0; i < JCList.length; i ++) {
            
            // 마커 이미지의 이미지 크기
            var imageSize = new kakao.maps.Size(24, 35); 
            
            // 마커 이미지를 생성   
            var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
            
            // 마커를 생성
            var marker = new kakao.maps.Marker({
                map: map, // 마커를 표시할 지도
                position: JCList[i].latlng, // 마커를 표시할 위치
                title : JCList[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
                image : markerImage // 마커 이미지 
            });

            // 마커에 클릭이벤트를 등록
            kakao.maps.event.addListener(marker, 'click', makeClickListener(map, marker));
        }
    }
}

// 출발지 / 도착지를 선택하는 상태일 경우, 선택된 마커로 출발지 / 도착지를 갱신.
function makeClickListener(map, marker) {
    return function() {
        if(SelectingDestination){
            document.getElementById("validationDefaultDestination").value = marker.Gb;
        }
        else if(SelectingSource){
            document.getElementById("validationDefaultSource").value = marker.Gb;
        }
        SelectingDestination = false;
        document.getElementById("ToggleDest").innerText = "도착지 변경";
        SelectingSource = false;
        document.getElementById("ToggleSource").innerText = "출발지 변경"; //.value = "출발지 변경";
    };
}

// JCList에 대해 Color 색상으로 지도에 선을 JC들을 지나는 선을 그림
function printLine(JCList, Color){
    if(JCList != null){
        for(var i = 0; i < Highways.length; i++){
            var linePath = []
            JCList.forEach((item) => {
                linePath.push(item.latlng);
            });
            var polyline = new kakao.maps.Polyline({
                path: linePath, // 선을 구성하는 좌표배열 입니다
                strokeWeight: 5, // 선의 두께 입니다
                strokeColor:  Color, // 선의 색깔입니다
                strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
                strokeStyle: 'solid' // 선의 스타일입니다
            });
            
            // 지도에 선을 표시합니다 
            polyline.setMap(map);  
        }
    }
}
// str(List)로 전달된 JC 리스트를 JC 이름 배열로 변환
function extractJC(JCs){
    var toReturn = JCs.toString().replace(/\[|\]|"|'| /g,'').split(',');
    toReturn.forEach((item) => {item.trim()});
    return toReturn;
}
// 출발지 변경 버튼 눌림 시퀀ㅅ
function SelectSource(){
    if(SelectingDestination){
        SelectingDestination = false;
        document.getElementById("ToggleDest").innerText = "도착지 변경";
    }
    SelectingSource = !SelectingSource;
    if(SelectingSource){
        document.getElementById("ToggleSource").innerText  = "취소";;//.value = "취소";
    }
    else{
        document.getElementById("ToggleSource").innerText  = "출발지 변경";
    }
}
// 도착지 변경 버튼 눌림 시퀀스
function SelectDestination(){
    if(SelectingSource){
        SelectingSource = false;
        document.getElementById("ToggleSource").innerText = "출발지 변경"; //.value = "출발지 변경";
    }
    SelectingDestination = !SelectingDestination;
    if(SelectingDestination){
        document.getElementById("ToggleDest").innerText  = "취소";
    }
    else{
        document.getElementById("ToggleDest").innerText = "도착지 변경";
    }
}