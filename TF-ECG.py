import numpy as np
import matplotlib.pyplot as plt

# Função para gerar um sinal ECG normal 
def gerarSinalECG(fs=1000, duration=5, heart_rate=72):
    t = np.linspace(0, duration, duration * fs)
    f_hr = heart_rate / 60.0
    
    # Onda QRS
    qrs_wave = np.zeros_like(t)
    qrs_wave[(t % (1/f_hr) < 0.02)] = 1  # Pico da onda QRS

    # Onda P
    p_wave = 0.02 * np.sin(2 * np.pi * 5 * t) * (t % (1/f_hr) < 0.1)

    # Onda T
    t_wave = 0.05 * np.sin(2 * np.pi * 1 * (t - 0.2)) * (t % (1/f_hr) > 0.2)

    # Sinal final combinando as ondas P, QRS e T
    ecg_signal = p_wave + qrs_wave + t_wave
    noise = np.random.normal(0, 0.005, len(t))
    ecg_signal += noise

    return ecg_signal

# Função para gerar um sinal ECG com frequência intrusa
def gerarSinalECGComProblema(fs=1000, duration=5, heart_rate=72, intrusao_freq=10.0):
    t = np.linspace(0, duration, duration * fs)
    f_hr = heart_rate / 60.0
    
    # Onda QRS
    qrs_wave = np.zeros_like(t)
    qrs_wave[(t % (1/f_hr) < 0.02)] = 1

    # Onda P
    p_wave = 0.02 * np.sin(2 * np.pi * 5 * t) * (t % (1/f_hr) < 0.1)

    # Onda T
    t_wave = 0.05 * np.sin(2 * np.pi * 1 * (t - 0.2)) * (t % (1/f_hr) > 0.2)

    # Sinal final combinando as ondas P, QRS e T
    ecg_signal = p_wave + qrs_wave + t_wave

    # Adicionar uma frequência intrusa mais pronunciada
    intrusao = 0.15 * np.sin(2 * np.pi * intrusao_freq * t)  # Aumentar a amplitude da intrusão
    ecg_signal += intrusao

    noise = np.random.normal(0, 0.005, len(t))
    ecg_signal += noise

    return ecg_signal

# Função para calcular a TF e encontrar a frequência dominante
def calcular_transformada(ECG, N, fs):
    ECG = ECG - np.mean(ECG)  # Remover a média para evitar deslocamento
    T = 1 / fs
    t = np.arange(0, N / fs, T)

    f = np.fft.fftfreq(N, T)
    transf = np.abs(np.fft.fft(ECG))

    return f, transf

# Função principal
def main():
    fs = 1000  # Frequência de amostragem
    duration = 5  # Duração do sinal em segundos
    heart_rate = 72  # Frequência cardíaca em BPM

    # Gerar o sinal de ECG normal ou sinal com problema
    #ECG = gerarSinalECG(fs=fs, duration=duration, heart_rate=heart_rate)  # Sinal normal
    ECG = gerarSinalECGComProblema(fs=fs, duration=duration, heart_rate=heart_rate, intrusao_freq=10.0)  # Sinal com problema

    N = len(ECG)
    f, transf = calcular_transformada(ECG, N, fs)

    # Manter apenas frequências positivas
    f_pos = f[:N//2]
    transf_pos = transf[:N//2]

    # Encontrar a frequência dominante (ignorar 0 Hz)
    indice_frequencia_dominante = np.argmax(transf_pos)
    frequencia_dominante = f_pos[indice_frequencia_dominante]
    bpm = frequencia_dominante * 60

    # Plotar os gráficos
    fig1, axs = plt.subplots(1, 1)
    axs.plot(ECG)
    axs.set_title("Sinal de ECG (Amostras)")
    axs.set_xlabel("Amostras")
    axs.set_ylabel("Amplitude")

    fig2, axs2 = plt.subplots(1, 1)
    axs2.plot(np.arange(0, N / fs, 1/fs), ECG)
    axs2.set_title("Sinal de ECG (Tempo)")
    axs2.set_xlabel("Tempo (s)")
    axs2.set_ylabel("Amplitude")

    fig3, axs3 = plt.subplots(1, 1)
    axs3.plot(f_pos, transf_pos)
    #axs3.axvline(x=frequencia_dominante, color='r', linestyle='--', label=f"Freq: {frequencia_dominante:.2f} Hz | BPM: {bpm:.2f}")
    axs3.set_title("Espectro de Frequências do ECG (Transformada de Fourier)")
    axs3.set_xlabel("Frequência (Hz)")
    axs3.set_ylabel("Amplitude")
    axs3.legend()

    plt.show()

# Executar o código principal
if __name__ == "__main__":
    main()
