import asyncio
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "7752728135:AAGiv_zHO6_ZtPG-sSMr7ELLygxXDSnw7pU"
USUARIO_SUPORTE = -1002771102722

GRUPOS_MONITORADOS = {
    -1002845390460: "GOZEI",
    -1001232222222: "ACERVO",
    -1002761227319: "OCEAN",
    -1002830038820: "HOTPLUS",
    -1002848362049: "CISEX",
    -1002843271683: "XHUB",
    -1002854541023: "OCULTO",
    -1002889555429: "COVIL",
}

produtos = [
    (
        "🔥 VIP Vazados 🔥",
        "R$ 19,90",
        "https://app.pushinpay.com.br/service/pay/9F4853DC-0842-4F83-BCF8-761261D47053",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://vizinhotv.com.br/wp-content/uploads/2024/05/WhatsApp-Image-2024-05-20-at-19.24.39-768x537.jpeg"
    ),
    (
        "😈 VIP GPs de Luxo 😈",
        "R$ 19,90",
        "https://app.pushinpay.com.br/service/pay/9F4853DC-0842-4F83-BCF8-761261D47053",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://www.fotoscaiunanet.com/wp-content/uploads/2018/02/Fotos-de-garotas-de-programas-peladas-e-gostosas-4.jpeg"
    ),
    (
        "🙈 VIP Casais & Cornos 🙈",
        "R$ 14,90",
        "https://app.pushinpay.com.br/service/pay/9f4fd7f0-b299-42a3-a6d6-97ccabe6a7e5",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://www.pornolandia.xxx/media/videos/tmb/54329/1.jpg"
    ),
    (
        "🥵 VIP Amadoras 🥵",
        "R$ 9,90",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://cnnamador.com/contents/videos_sources/284000/284009/posters/1.jpg"
    ),
    (
        "🔞 VIP Novinhas 🔞",
        "R$ 29,90",
        "https://app.pushinpay.com.br/service/pay/9F4851AC-8054-4E0E-BE14-19455A348FE1",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://www.mixputaria.com/videos/wp-content/uploads/2023/06/caiu-na-net-Novinha-tocando-siririca.jpg"
    ),
    (
        "🏳‍🌈 VIP Trans 🏳‍🌈",
        "R$ 29,90",
        "https://app.pushinpay.com.br/service/pay/9F4851AC-8054-4E0E-BE14-19455A348FE1",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://cnnamador.com/contents/videos_screenshots/286000/286764/preview.jpg"
    ),
    (
        "🎶 VIP Funk 🎶",
        "R$ 14,90",
        "https://app.pushinpay.com.br/service/pay/9f4fd7f0-b299-42a3-a6d6-97ccabe6a7e5",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://ei-ph.rdtcdn.com/videos/202307/03/434762611/original/(m=eag28f)(mh=TWlegIZs6qI2KhC6)0.jpg"
    ),
    (
        "🤳🏻 VIP Lives 🤳🏻",
        "R$ 19,90",
        "https://app.pushinpay.com.br/service/pay/9F4853DC-0842-4F83-BCF8-761261D47053",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://tubepussy.org/contents/videos_screenshots/2000/2833/preview.jpg"
    ),
    (
        "😈 VIP Omegle 😈",
        "R$ 19,90",
        "https://app.pushinpay.com.br/service/pay/9F4853DC-0842-4F83-BCF8-761261D47053",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://t99.nudevista.com/258/102554258.b.jpg"
    ),
    (
        "👫 VIP Incesto 👫",
        "R$ 9,90",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://novinhaspelada.com/wp-content/uploads/2023/11/Vovo-fodendo-a-bucetinha-da-netinha-310x190.jpg"
    ),
    (
        "🔵 VIP Privacy + Onlyfans 🔵",
        "R$ 29,90",
        "https://app.pushinpay.com.br/service/pay/9F4851AC-8054-4E0E-BE14-19455A348FE1",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://www.mixputaria.com/videos/wp-content/uploads/2024/01/Catarina-Paolino-vazado-do-Onlyfans-2024.jpg"
    ),
    (
        "⚜️ VIP Famosinhas ⚜️",
        "R$ 19,90",
        "https://app.pushinpay.com.br/service/pay/9F4853DC-0842-4F83-BCF8-761261D47053",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://www.boabronha.com/wp-content/uploads/2022/11/mc-mirella-pelada_4.jpg"
    ),
    (
        "📸 VIP Cãmeras 📸",
        "R$ 14,90",
        "https://app.pushinpay.com.br/service/pay/9f4fd7f0-b299-42a3-a6d6-97ccabe6a7e5",
        "https://app.pushinpay.com.br/service/pay/9F484D59-0B3F-4BA0-A819-4C6B8396684C",
        "https://thumb-nss.xhcdn.com/a/pVrZibtMbmGHEUlmSX9iZQ/010/032/217/v2/2560x1440.206.webp"
    ),
]

CUPOM_VALIDO = "TUDO10"
user_data = {}
timers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{nome} - {preco}", callback_data=f"produto_{i}")]
        for i, (nome, preco, *_rest) in enumerate(produtos)
    ]
    # Alteração feita aqui: emojis inseridos diretamente para evitar erro de encoding
    await update.message.reply_text("🛍️ Escolha um VIP 👇", reply_markup=InlineKeyboardMarkup(keyboard))

async def produto_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    produto_id = int(query.data.replace("produto_", ""))
    nome, preco, *_rest, imagem_url = produtos[produto_id]

    user_data[user_id] = {"produto_id": produto_id, "etapa": "aguardando_cupom"}

    legenda = (
        f"🛒 <b>Produto selecionado:</b>\n\n"
        f"{escape(nome)}\n"
        f"💵 Preço: {escape(preco)}\n\n"
        f"Você tem um cupom para aplicar?"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Sim", callback_data="tem_cupom")],
        [InlineKeyboardButton("❌ Não", callback_data="sem_cupom")]
    ]

    await context.bot.send_photo(
        chat_id=user_id,
        photo=imagem_url,
        caption=legenda,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

    if user_id in timers:
        timers[user_id].cancel()
    timers[user_id] = asyncio.create_task(abandono_check(user_id, context.bot))

async def cupom_escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id in timers:
        timers[user_id].cancel()

    dados = user_data.get(user_id)
    if not dados:
        await context.bot.send_message(chat_id=user_id, text="❌ Erro interno. Envie /start novamente.")
        return

    produto_id = dados["produto_id"]
    nome, preco, link_normal, *_ = produtos[produto_id]

    if query.data == "sem_cupom":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💳 Produto: {nome}\nPreço: {preco}\n\nClique abaixo para pagar:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💵 PAGAR AGORA", url=link_normal)]])
        )
        await asyncio.sleep(10)
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🧾 <b>Fez o pagamento?</b>\nReceba seu acesso enviando o comprovante aqui: @cgsuporte",
            parse_mode="HTML"
        )
    else:
        await context.bot.send_message(chat_id=user_id, text="✍️ Digite seu cupom abaixo:")
        user_data[user_id]["etapa"] = "digitando_cupom"
        timers[user_id] = asyncio.create_task(abandono_check(user_id, context.bot))

async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    mensagem = update.message.text.strip()

    if user_id in timers:
        timers[user_id].cancel()

    dados = user_data.get(user_id)
    if not dados or dados.get("etapa") != "digitando_cupom":
        return

    produto_id = dados["produto_id"]
    nome, preco, link_normal, link_desconto, *_ = produtos[produto_id]

    if mensagem.upper() == CUPOM_VALIDO:
        await update.message.reply_text(
            f"✅ Cupom <b>{CUPOM_VALIDO}</b> aplicado com sucesso!\n\n{escape(nome)}\n💵 Novo preço: R$ 10,00\n\nClique abaixo para pagar:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 PAGAR COM DESCONTO", url=link_desconto)]]),
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            f"❌ Cupom inválido. Segue o valor original para pagamento:\n\n{escape(nome)}\n💵 Preço: {escape(preco)}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 PAGAR AGORA", url=link_normal)]]),
            parse_mode="HTML"
        )

    await asyncio.sleep(10)
    await context.bot.send_message(
        chat_id=user_id,
        text=f"🧾 <b>Fez o pagamento?</b>\nReceba seu acesso enviando o comprovante aqui: @supvipoficial",
        parse_mode="HTML"
    )

    user_data[user_id]["etapa"] = None

async def abandono_check(user_id, bot):
    try:
        await asyncio.sleep(5 * 60)
        dados = user_data.get(user_id)
        if not dados:
            return

        produto_id = dados["produto_id"]
        nome_produto, preco = produtos[produto_id][0], produtos[produto_id][1]

        try:
            user = await bot.get_chat(user_id)
            nome = user.full_name
            username = f"@{user.username}" if user.username else "(sem username)"
            fotos = await bot.get_user_profile_photos(user_id, limit=1)
            foto = fotos.photos[0][0].file_id if fotos.total_count > 0 else None
        except:
            nome = "Indefinido"
            username = "(erro ao obter info)"
            foto = None

        grupos_em_comum = []
        for chat_id, nome_grupo in GRUPOS_MONITORADOS.items():
            try:
                membro = await bot.get_chat_member(chat_id, user_id)
                if membro.status not in ("left", "kicked"):
                    grupos_em_comum.append(nome_grupo)
            except:
                continue

        texto_grupos = ", ".join(grupos_em_comum) if grupos_em_comum else "Nenhum grupo monitorado em comum"

        mensagem_html = (
            f"⚠️ <b>Lead abandonou o processo de compra!</b>\n\n"
            f"👤 Nome: {escape(nome)}\n"
            f"🔗 Username: {escape(username)}\n"
            f"🛍️ Produto: {escape(nome_produto)}\n"
            f"💰 Preço: {escape(preco)}\n"
            f"👥 Grupos em comum: {escape(texto_grupos)}"
        )

        if foto:
            await bot.send_photo(
                chat_id=USUARIO_SUPORTE,
                photo=foto,
                caption=mensagem_html,
                parse_mode="HTML"
            )
        else:
            await bot.send_message(
                chat_id=USUARIO_SUPORTE,
                text=mensagem_html,
                parse_mode="HTML"
            )

        try:
            keyboard = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🔓 Entrar no Canal VIP", url="https://t.me/+bzeWJOcg4NY2YzJh")
                ]]
            )

            await bot.send_message(
                chat_id=user_id,
                text=(
                    "👀 Percebi que você ainda não concluiu seu pedido.\n\n"
                    "💎 Vou te dar um VIP de graça...\n"
                    "✅ Dicas exclusivas\n"
                    "✅ Bônus secretos\n"
                    "✅ Descontos relâmpago\n\n"
                    "🎁 Só pra quem entrou no processo de compra e não finalizou, entre agora 👇🏻"
                ),
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Erro ao enviar mensagem de recuperação para {user_id}: {e}")

    except asyncio.CancelledError:
        pass

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(produto_handler, pattern="^produto_"))
app.add_handler(CallbackQueryHandler(cupom_escolha, pattern="^(tem_cupom|sem_cupom)$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

print("🤖 Bot rodando com monitoramento de abandono, cupom, grupos e foto de perfil.")
app.run_polling()
