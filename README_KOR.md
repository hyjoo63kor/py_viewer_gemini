# Png/Svg/Pdf 뷰어 (svgvvr)

PySide6를 기반으로 제작된 PNG, JPG, SVG, PDF 파일을 고화질로 감상할 수 있는 데스크톱 애플리케이션입니다.

## 주요 기능
- **다양한 포맷 지원**: PNG, JPG 이미지뿐만 아니라 SVG(벡터) 및 PDF 문서를 지원합니다.
- **고해상도 유지**: SVG와 PDF는 벡터 렌더링 방식을 사용하여 아무리 확대해도 글자나 그래픽이 깨지지 않고 선명하게 유지됩니다.
- **직관적인 조작**:
  - **줌 (Zoom)**: 마우스 휠 또는 상단 패널의 `[+]`, `[-]` 버튼 사용.
  - **이동 (Pan)**: 마우스 왼쪽 버튼 드래그 또는 상단 패널의 방향키 사용.
  - **페이지 이동**: PDF 파일의 경우 상단 패널의 `이전/다음` 버튼으로 페이지 탐색 가능.
- **드래그 앤 드롭**: 외부 파일을 앱 창으로 끌어다 놓아 즉시 로드할 수 있습니다.
- **파일 열기 버튼**: 📂 버튼을 통해 탐색기에서 파일을 직접 선택할 수 있습니다.

## 개발 및 실행 환경

### 사전 준비
[uv](https://github.com/astral-sh/uv)가 설치되어 있어야 합니다.

### 의존성 설치
```bash
uv sync
```

### 앱 실행
```bash
uv run py-viewer
```

### 빌드 (Windows 단일 실행 파일)
`dist/` 디렉토리에 `svgvvr.exe` 파일이 생성됩니다.
```bash
uv run pyinstaller app.spec
```

### 테스트 및 코드 품질 체크
```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

### 프로젝트 정리 (Clean)
빌드 생성물 및 각종 캐시 폴더를 삭제합니다.
```bash
uv run clean
```

## 프로젝트 구조
- `src/my_app/main.py`: 애플리케이션 메인 로직 및 UI 구현
- `src/my_app/clean.py`: 프로젝트 정리 스크립트
- `app.spec`: PyInstaller 빌드 설정 파일
- `pyproject.toml`: 프로젝트 메타데이터 및 의존성 관리
