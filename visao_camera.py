"""Protótipo do módulo de visão do sistema de ponto por QR Code.

Abre a câmera, detecta QR Codes em tempo real e, a cada leitura, registra o
horário com feedback visual (overlay verde) e sonoro (beep). Primeiro passo do
projeto descrito em docs/ROADMAP.md.

O conteúdo do QR Code e o horário ainda não são persistidos: a leitura só aparece
no terminal e na tela. Durante a confirmação, novas leituras são ignoradas.
"""

import argparse
import time
from datetime import datetime

import cv2

# Feedback sonoro multiplataforma: winsound no Windows, bell ANSI nos demais.
try:
    import winsound

    def emitir_beep(frequencia: int = 1000, duracao: int = 300) -> None:
        winsound.Beep(frequencia, duracao)
except ImportError:  # Linux / macOS

    def emitir_beep(frequencia: int = 1000, duracao: int = 300) -> None:
        print("\a", end="", flush=True)


DURACAO_CONFIRMACAO = 3  # segundos que o overlay de confirmação fica na tela


def inicializar_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """Abre a câmera indicada; levanta RuntimeError se ela não estiver disponível."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Erro ao abrir a câmera (índice {camera_index})")
    return cap


def criar_detector_qr() -> cv2.QRCodeDetector:
    """Cria o detector de QR Code do OpenCV."""
    return cv2.QRCodeDetector()


def capturar_frame(cap: cv2.VideoCapture):
    """Lê o próximo frame; levanta RuntimeError se a leitura falhar."""
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Erro ao capturar frame")
    return frame


def detectar_qr_code(detector: cv2.QRCodeDetector, frame):
    """Retorna (texto, contorno) do QR Code.

    O contorno é None se nada foi detectado. O texto pode vir vazio mesmo com
    contorno, quando o código foi localizado mas não decodificado.
    """
    data, bbox, _ = detector.detectAndDecode(frame)
    return data, bbox


def desenhar_retangulo_qr(frame, bbox) -> None:
    """Desenha o contorno do QR Code sobre o frame, em verde."""
    pontos = bbox[0].astype(int)
    cv2.polylines(frame, [pontos], True, (0, 255, 0), 3)


def criar_overlay_verde(frame):
    """Retorna um frame totalmente verde (peso 1.0 no overlay e 0.0 na imagem)."""
    overlay = frame.copy()
    overlay[:] = (0, 255, 0)
    return cv2.addWeighted(frame, 0.0, overlay, 1.0, 0)


def exibir_texto_ponto(frame, hora: datetime) -> None:
    """Escreve o horário do registro no meio do frame."""
    texto = f"Ponto marcado as {hora.strftime('%H:%M:%S')}"
    cv2.putText(
        frame,
        texto,
        (50, frame.shape[0] // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
    )


def verificar_tecla_saida() -> bool:
    """Indica se 'q' foi pressionada. O waitKey também faz a janela ser atualizada."""
    return cv2.waitKey(1) & 0xFF == ord("q")


def exibir_frame(frame, titulo: str = "Detector de QR Code") -> None:
    """Mostra o frame na janela da aplicação."""
    cv2.imshow(titulo, frame)


def liberar_recursos(cap: cv2.VideoCapture) -> None:
    """Libera a câmera e fecha as janelas do OpenCV."""
    cap.release()
    cv2.destroyAllWindows()


def esta_no_periodo_confirmacao(current_time: float, qr_detected_time: float) -> bool:
    """Indica se ainda está na confirmação, período em que não há novas leituras."""
    return current_time - qr_detected_time < DURACAO_CONFIRMACAO


def parse_args() -> argparse.Namespace:
    """Lê os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description="Detector de ponto por QR Code.")
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Índice da câmera a ser usada (padrão: 0).",
    )
    return parser.parse_args()


def main() -> None:
    """Laço principal: captura, exibe a confirmação ou procura um novo QR Code."""
    args = parse_args()
    cap = inicializar_camera(args.camera)
    detector = criar_detector_qr()

    print("Pressione 'q' para sair")
    print("Aproxime um QR Code da câmera para detectar")

    qr_detected_time = 0.0
    last_qr_data = ""
    hora_registro = None

    try:
        while True:
            frame = capturar_frame(cap)
            current_time = time.time()

            if hora_registro and esta_no_periodo_confirmacao(current_time, qr_detected_time):
                frame = criar_overlay_verde(frame)
                exibir_texto_ponto(frame, hora_registro)
            else:
                if last_qr_data:
                    print("Pronto para escanear novamente...")
                    last_qr_data = ""

                data, bbox = detectar_qr_code(detector, frame)

                if bbox is not None:
                    desenhar_retangulo_qr(frame, bbox)

                    if data:
                        print(f"QR Code detectado: {data}")
                        emitir_beep()
                        last_qr_data = data
                        qr_detected_time = current_time
                        hora_registro = datetime.now()

            exibir_frame(frame)

            if verificar_tecla_saida():
                break
    finally:
        liberar_recursos(cap)


if __name__ == "__main__":
    main()
