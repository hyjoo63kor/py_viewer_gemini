# Png/Svg/Pdf/Markdown Viewer

PySide6 (Qt6) 기반의 경량 데스크톱 파일 뷰어입니다.  
PNG, JPG, SVG, PDF, Markdown 파일을 하나의 창에서 볼 수 있습니다.

## 주요 기능

- **다중 포맷 지원** — PNG, JPG, SVG(벡터), PDF(QtPdf 벡터 렌더링), Markdown(HTML 렌더링)
- **고품질 렌더링** — SVG와 PDF는 어떤 줌 레벨에서도 선명하게 유지
- **인터랙티브 컨트롤**
  - 줌: 마우스 휠 또는 [+] / [-] 버튼
  - 패닝: 마우스 드래그 또는 방향 버튼
  - PDF 페이지 이동: Prev/Next 버튼, PgUp/PgDn 키
  - Markdown 스크롤: PgUp/PgDn 키
- **드래그 앤 드롭** — 지원되는 파일을 창에 끌어다 놓으면 바로 열림
- **파일 열기 버튼** — 카테고리별 필터가 있는 파일 선택 대화상자
- **상태 표시줄** — 로드된 파일 경로 또는 에러 메시지 표시
- **앱 아이콘** — 윈도우 타이틀바와 빌드된 실행 파일에 커스텀 아이콘 적용

## 지원 포맷

| 포맷 | 확장자 | 뷰어 |
|------|--------|------|
| 래스터 이미지 | `.png`, `.jpg`, `.jpeg` | GraphicsViewer (QGraphicsView) |
| 벡터 이미지 | `.svg` | GraphicsViewer (QGraphicsSvgItem) |
| PDF 문서 | `.pdf` | PdfViewer (QPdfView) |
| Markdown | `.md`, `.markdown` | MarkdownViewer (QTextBrowser) |

## 요구 사항

- Python 3.12 이상
- [uv](https://github.com/astral-sh/uv) 패키지 매니저

## 시작하기

### 의존성 설치

```bash
uv sync
```

### 앱 실행

```bash
uv run app
```

### 단독 실행 파일 빌드 (Windows)

`dist/` 디렉토리에 앱 아이콘이 포함된 `svgvvr.exe`가 생성됩니다.

```bash
uv run pyinstaller app.spec
```

### 린트 & 타입 체크

```bash
uv run ruff check .
uv run mypy src/my_app/
```

### 테스트 실행

```bash
uv run pytest tests/ -v
```

### 빌드 산출물 정리

```bash
uv run clean
```

## 프로젝트 구조

```
├── assets/
│   ├── icon.svg          # 앱 아이콘 (SVG 원본)
│   └── icon.ico          # 앱 아이콘 (Windows ICO, 멀티사이즈)
├── src/my_app/
│   ├── main.py           # 앱 진입점 및 모든 뷰어 클래스
│   ├── clean.py          # 빌드 산출물 정리 스크립트
│   └── __init__.py
├── tests/
│   ├── conftest.py       # pytest-qt 픽스처
│   └── test_main.py      # 단위 테스트
├── app.spec              # PyInstaller 빌드 설정
├── pyproject.toml        # 프로젝트 설정 및 의존성
└── README.md
```

## 키보드 단축키

| 키 | 동작 |
|----|------|
| PgDn | PDF: 다음 페이지 / Markdown: 아래로 스크롤 |
| PgUp | PDF: 이전 페이지 / Markdown: 위로 스크롤 |
| Ctrl + 마우스 휠 | Markdown: 줌 인/아웃 |
| 마우스 휠 | 이미지/SVG/PDF: 줌 인/아웃 |

## 라이선스

자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
