from groq import Groq

client = Groq(api_key="")

print("Iniciando Agente no Groq (Llama 3.3)...")

try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "user",
                "content": "Escreva 'Vitoria Final no Groq' e uma frase sobre persistência técnica.",
            }
        ],
    )

    texto = completion.choices[0].message.content
    print(f"\n[SUCESSO!] O Groq respondeu:\n{texto}")

    with open("vitoria_groq.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print("\n✅ Arquivo 'vitoria_groq.txt' criado!")

except Exception as e:
    print(f"Erro no Groq: {e}")