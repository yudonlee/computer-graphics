# Obj Viewer & drawing hierarchical model

크기가 1인 정사각형만이 렌더링되었던 Project1과 달리, 하나의 Obj파일을 렌더링한다. 이때 렌더링을 원하는 파일을 실행중인 윈도우에 드래그한다.

# 실행 환경

Python 3.9.3  
numpy  
glfw

# 기능설명

# 1. Single Mesh Rendering Mode

- 기존에 ClassAssignment1에서 구현된 Orbit, Panning, Zooming 기능이 지원됩니다.

- 렌더링시, singleMesh()라는 함수가 호출되어 드래그된 obj 파일의 데이터를 불러오고 실행 윈도우에 draw하게 됩니다.

## 1) Flat shading vs Smooth Shading

default mode는 Flat shading이며, key 's'를 통해서 두개 모드를 번갈아가며 사용하는 것이 가능합니다.

- draw()함수에서, 파싱된 데이터 정보들을 flat shading or smoothshading으로 렌더링하게 됩니다. flat shading mode에서는 glDrawArray(), smooth shading의 경우 glDrawElements()를 이용합니다.

- smoothShading은 각 vertex의 해당되는 모든 normal vertex를 더한 뒤, 크기로 나눈 결과로 발생한 vertex를 Normal vertex로 지정합니다.

- 이때 polygon optimization을 위해, quad 이상의 polygon들은 triangulation algorithm을 이용하여 4개 이상의 vertex로 이루어진 face를 분리합니다.

|                                         Flat Shading                                         |                                               Smooth Shading                                               |
| :------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------: |
| ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment2/Image/boat.png) | ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment2/Image/afterSmoothShading.png) |

## 2) WireFrame mode

renderintl, default는 glPolygonMode에서 GL_LINE으로 설정되며, key 'z'가 입력된다면 GL_FILL이 활성화되어 wireframe mode가 종료됩니다.

|                                            WireFrame mode                                             |                                         Normal Mode                                          |
| :---------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------: |
| ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment2/Image/wireframeMode.png) | ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment2/Image/boat.png) |

# 2. Animating hierarchical model render mode

key 'h'를 누를 시, animating hierarhcical mode가 작동되어, 계층구조로 설정된 "Boat"가 렌더링됩니다.
전체적인 구성은 바다를 가르는 보트를 형상화했습니다.
해당 boat는 anchor, motor_fan, rope등으로 구성됩니다
![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment2/Image/hierarchicalStructure.jpeg)

- 위 그림과 같이 본 계층구조 모델은, root인 boat를 기준으로 이루어집니다. matrix stack에 따라, root인 boat가 움직이면 anchor, motor_fan, rope등이 동일하게 움직입니다.
- moter_fan은 root인 boat에 따라 움직이는 동시에, rotate의 모션이 추가되어 움직이는 모터팬의 모션이 나타납니다.
- root의 또다른 child인 rope는 anchor과 함께 움직이며, anchor는 별도로 또다른 모션을 취하게 됩니다. rope의 자체적인 움직임은 물살에 의해 rotate되며, 이렇게 물살을 가를때 anchor는 더 깊이 존재하기 때문에 rotation각도를 크게 했습니다.

# 3. Animation 결과

<img width="80%" src="https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment2/Image/animation.gif"/>
