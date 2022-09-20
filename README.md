<h1>프로젝트 개요</h1>
<a href="https://docs.google.com/presentation/d/1ghOqb4nP-iMGkwy4UO7RU-bNc0rMU-mB38UIWu2qxWI/edit#slide=id.g152ed7f1621_1_13">팀 보고서</a>

<a href="https://www.youtube.com/watch?v=dCie5xD8FBA">발표 영상</a>

<h3>🎯프로젝트 목적</h3>
  <ul>
    <li>퍼스널 모빌리티(이하 PM)의 수요를 예측하고 이를 실시간 지도에 반영하여 공급의사결정을 내리는 것에 도움을 준다.</li>
    <li>헬멧 인증 및 주차 인증 마일리지 적립 서비스를 도입하여 안전하고 바람직한 PM 사용자 문화를 만든다.</li>
    <li>사고 시 대처 요령을 편리한 형태로 제공해 사용자와 서비스 간의 신뢰성을 구축한다.</li>
  </ul>

<h3>🤫프로젝트 배경</h3>
  <ul>
    최근 PM의 공유서비스 활성화로 인해 이용률이 증가함에 따라, 이를 공급하는 업체의 서비스를 비롯하여 안전성에 대한 관심이 높아지고 있다.
    따라서, 본 프로젝트에서는 데이터를 통한 PM관련 수요예측, 이미지 탐지 등을 개발하여 PM의 공급자와 사용자 모두에게 이익이 될 수 있는 서비스를 제공하고자 한다.
  </ul>

<h3>🛴서비스 기능</h3>
  <ul>
    <li>Personal mobility 수요예측 기능(VAR 모델)</li>
    <li>헬멧/주차 인증 서비스(Yolo v5 모델)</li>
    <li>사고 대처 요령 안내</li>
  </ul>

<br>
<br>

<h1>담당 파트 설명</h1>
  <h4> - 헬멧/주차 인증 서비스 시 입력되는 유저 데이터를 DB에 적재<br>
   - ML/DL 모델 서빙<br>
   - 웹 구축</h4>

<br>


<table>
	<th>skill</th>
	<th>version</th>
	<tr>
	    <td>개발환경</td>
	    <td>MacOS M1</td>
	</tr>
	<tr>
	    <td>IDE</td>
	    <td>VSCode</td>
	</tr>
  	<tr>
	    <td>개발 Framework</td>
	    <td>Django4.1.1</td>
	</tr>
  	<tr>
	    <td>프로그래밍 언어</td>
	    <td>Python 3.9.12</td>
	</tr>
  	<tr>
	    <td>DataBase</td>
	    <td>MySQL3.0.28(AWS RDS)</td>
	</tr>
  	<tr>
	    <td>배포환경</td>
	    <td>AWS</td>
	</tr>
    </table>
    
<br>

  <ul>
    <li>개발은 전체적으로 MacOS M1+VSC에서 진행되었다.</li>
    <li>프레임워크과 언어는 최신 버전을 사용했으나 Python 같은 경우는 3.10.#으로 할 경우 딥러닝 모델을 위한 패키지와 충돌이 생겨 3.9.# 으로 진행되었다.</li>
    <li>유저정보와 인증 사진을 입력받아 저장하기 위해 DB는 MySQL을 사용하였다. PM 수요 예측 모델에서 서울시 따릉이 데이터를 사용하기 위해 MySQL에 넣어달라는 요청에 400MB 정도의 데이터를 적재하였다.</li>
    <li>배포 환경은 AWS EC2를 이용해 Ubuntu와 CentOS7 서버에서 실행하려고 시도하였으나 패키지간의 충돌과 프리티어 요금으로 Yolo v5 모델의 용량을 감당할 수 없어 실패했다.</li>
  </ul>

<br>
<br>

<h1>홈페이지 구조</h1>

<img width="180" alt="image" src="https://user-images.githubusercontent.com/95471902/191154667-c92da068-aeae-4b10-ac9e-9944cf167c51.png">

<br>
  <ul>
  <li>내비바부터 Footer의 모든 버튼을 눌러도 해당 페이지로 이동하게 설계하였다.</li>
  <li>기능에는 총 4가지 기능 페이지로 이동할 수 있도록 짰으며, 각각 필요한 정보를 입력하면 ML/DL 모델이 결과값을 리턴해주는 구조이다.</li>
  <li>Team과 Contact칸에서는 팀원들의 소개와 각각의 Github과 Email로 넘어갈 수 있도록 링크를 걸어두었다.</li>
  </ul>
  
  
  ![image](https://user-images.githubusercontent.com/95471902/191154930-6ffb50f9-7d06-40a5-bbab-5ae0c2ede313.png)

<br>
<br>

<h1>개선점 및 회고</h1>
<h4>1. 로그인 기능</h4>
  <ul>
    <li>로그인 기능을 추가해 기존 회원들은 바로 정보가 입력되게 하고 싶다.</li>
  </ul>

<h4>2. 데이터 파이프라인</h4>
  <ul>
    <li>수요 예측 기능에서 ML 모델이 시계열 모델이었는데, 이미 있는 1월~6월까지의 데이터만 가지고 이미 알고 있는 7월의 데이터와의 차이를 계산하는 형태였다(7월 실제치-7월 예측치).</li>
    <li>실시간 따릉이 데이터를 가져와 `데이터 파이프라인`을 만들고 그것을 추출해 다른 컬럼들을 가지고 예측하는 ML 모델을 짜봐도 좋지 않았을까 싶다.</li>
  </ul>
<h4>3. DL 모델의 경량화</h4>
  <ul>
    <li>헬멧/주차 인증 파트에서 DL 모델이 Yolo v5여서 OpenCV로 쉽게 임포트 해와서 할 수가 없이 Pytorch hub를 전체 작업 폴더에 넣어야 해서 전체 용량이 너무 커져버렸다. </li>
    <li>좀 더 쉬운 모델을 써서 경량화를 해보고 싶다.</li>
  </ul>
<h4>4. 챗봇 기능</h4>
  <ul>
    <li>사고 대처 안내 기능에서 원래는 챗봇 기능을 넣고 싶었으나, 그만한 법률 내용도 많이 없었고(신생법이라), 시간이 부족해 단순히 입력값을 선택하면 if문으로 결과문을 리턴하는 형태가 되었다. </li>
    <li>좀 더 깜찍한 UI를 짜서 진짜 챗봇같은 기능을 구현해보고 싶다.</li>
  </ul>
<h4>5. 배포</h4>
  <ul>
    <li>배포하고싶다. 배포를 하지 못 한 이유는 내 생각엔 아래와 같다.</li>
      <ul>
        <li>AWS에 익숙하지 않다.</li>
        <li>Linux 서버에 익숙하지 않았다.</li>
        <li>ML모델과 DL모델에서 원하는 Python 버전이 달랐다.(DL이 3.9 미만을 원했는데 ML은 높을 수록 좋았다)</li>
        <li>Yolo v5의 폴더가 너무 컸다.</li>
      </ul>
  </ul>
