#!/usr/bin/env python3
"""Build wdytai.app: index (en), zh/ (zh-Hant), cn/ (zh-Hans), privacy/, terms/, support/.
Layout mirrors fluentin.app / lossic.app: sticky nav, centred hero with h1 + badge + phone
shot rotator, feature grid, numbered steps, confidence strip, privacy card, disclaimer, FAQ,
bottom CTA, footer. CSS lives in scripts/_css.txt (fluentin's, re-tinted to the WDYT blue).

    python3 scripts/build.py
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://wdytai.app"
MAIL = "tautiu.dev+wdyt@gmail.com"
LAST_UPDATED = "September 18, 2026"
CSS = (ROOT / "scripts/_css.txt").read_text()
STORE_URL = None   # not on the App Store yet → dashed "coming soon" badge

T = {
 "en": dict(
  lang="en", path="/", title="WDYT — What do you think? Say it, confirm it, decide.",
  desc="WDYT turns a half-formed thought — a few spoken words, maybe a photo of a menu — into a clear question with options you confirm, then a decision with honest confidence.",
  nav=["Features", "How it works", "FAQ"], nav_ids=["features", "how", "faq"],
  h1='You don\'t have to know what you\'re asking.<br>Just <em>say it</em>.',
  sub="Hold the button, mumble what you're weighing, snap the menu if there is one. WDYT works out the actual question and the options, shows them to you to fix, and only then gives you an answer — with a number for how sure it is.",
  badge="iPhone · coming to the App Store", shots=("shot-en.jpg", "shot-zh.jpg", "shot-cn.jpg"),
  features_title="Why it feels different",
  features=[("Speak, don't type", "Hold or tap the mic and talk. English through Apple's recogniser; Chinese through SenseVoice running on your phone. No audio ever leaves the device."),
            ("It phrases the question for you", "A generator model reads your words and photos and writes the question, the options, and what it saw — you never fill in a form."),
            ("You stay in charge", "Nothing is decided until you've looked. Edit the question, delete an option, add one it missed, correct what it read off the photo. Then confirm."),
            ("A decision, not an essay", "The answer comes from TypeSafe's Jev, a model that returns a typed choice with calibrated probabilities in under half a second — no rambling."),
            ("Honest about uncertainty", "When it's 55/45, it says so. When you gave it nothing to go on, it says that too, and lets you add one sentence and ask again."),
            ("It learns you, if you let it", "Two plain files — identity.md and soul.md — hold who you are and how you decide. Off by default; when on, they're revised after each answer and you can edit them any time.")],
  how_title="Three steps, one tap each", how_sub="Understand → confirm → decide. The decision model is only called after you confirm.",
  steps=[("Say it (and show it)", "“What should I eat…” plus a photo of the menu. Up to three photos; they're resized on the phone before anything is sent."),
         ("Check what it understood", "The question in one sentence, the options with a line each, and “what I saw” from your photos. Fix anything. Nothing has been decided yet."),
         ("Confirm and get the answer", "One pick, the probability of every option, a confidence figure, and one line on why. Add a sentence and ask again if it missed something.")],
  verdicts=[("ok", "92% — clear", "Preferences and options line up; take it."), ("close", "55% — coin flip", "Told as a coin flip, not dressed up as certainty."), ("no", "Not enough to go on", "It says so and asks for one more sentence.")],
  privacy_h="Your keys. Your phone. No WDYT servers.",
  privacy_p=f'WDYT has no backend. Speech is recognised on the device. Understanding goes straight from your phone to Google Gemini with your own API key; the decision goes straight to OpenRouter (TypeSafe Jev) with your own key. Keys live in the iOS Keychain. <a href="/privacy/">Privacy policy</a> · <a href="/terms/">Terms</a>',
  disclaim_b="For fun, not for life decisions.",
  disclaim_p="WDYT is entertainment. Its answers come from AI models and can be wrong. For anything that matters — health, money, legal matters, safety, relationships, work — consult a qualified professional and use your own judgment. You use it at your own risk; the app and its developer are not responsible for any decision made with it or any loss arising from one.",
  faq_title="Questions",
  faq=[("Why two API keys?", "Two different jobs. Gemini (Google) reads your words and photos and writes the question — you need a Gemini key from Google AI Studio. Jev (TypeSafe) makes the decision — it's reached through OpenRouter, so you need an OpenRouter key. Both are pay-as-you-go on your own account; a typical question costs well under a cent. WDYT never sees either key."),
       ("What is Jev, and why not just ask Gemini to decide?", "Jev is a “System One” model from TypeSafe: it doesn't generate text, it returns a typed answer — one option from your list, a yes/no probability, or a position on a scale — with calibrated probabilities, in about 100–500 ms. That's what makes the confidence figure meaningful and the answer instant. Gemini is used for the part Jev can't do: understanding fuzzy speech and reading photos."),
       ("Does the decision model see my photo?", "No — Jev is text-only. Gemini writes down everything it saw (every menu item with its price, what the outfit looks like) and that text is what Jev judges. You see that text on the confirm screen and can correct it."),
       ("Which languages?", "The interface is English, 繁體中文 or 简体中文 — your choice, independent of the phone's language. Speech: English via Apple; Mandarin via SenseVoice after a one-time ~230 MB download. The model is shared with other tautiu.dev apps on your phone, so you only download it once."),
       ("What are identity.md and soul.md?", "identity.md is who you are — diet, budget, habits. soul.md is how you decide — what you optimise for, what you avoid. Both are sent with every question so answers fit you. You can write them yourself, or turn on “update these from my questions” and let Gemini revise them after each answer. Off by default."),
       ("Is anything stored or shared?", "Everything stays on your phone: keys in the Keychain, the two profile files, your history. The only network calls are the two you initiate, from your phone directly to Google and OpenRouter under their privacy policies.")],
  cta_h="Stop overthinking lunch.", cta="Coming to the App Store",
  footer_privacy="Privacy", footer_terms="Terms", footer_support="Support",
  demo=dict(title="WDYT", storyTabs=["Menu","Outfit","Gym"],
  outfit=dict(pick="Add photos", pickHint="Up to three", garments=[("Navy blazer","navy"),("Beige knit","beige"),("Black dress","black")],
       typed="which one for tomorrow's interview…", understood="Here's what I think you're asking", q="Which outfit should I wear to tomorrow's interview?",
       opts=[("Navy blazer","$— · formal, sharp"),("Beige knit","$— · soft, approachable"),("Black dress","$— · elegant, simple"),("None of these","")], doomed=None,
       saw="What I picked up", sawText="Three photos on a bed: a navy single-breasted blazer with a white shirt, slim fit; an oversized beige ribbed knit; a black knee-length sheath dress. You said the interview is at a design studio.",
       know="What I know about you", knowText="identity.md: product designer · soul.md: would rather look understated than overdressed",
       confirm="Confirm and get the answer", answer="Navy blazer", conf="confidence 78%", probs=[("Navy blazer",78),("Black dress",15),("Beige knit",7),("None of these",0)],
       why="Formal enough for a first meeting, but the shirt-and-blazer keeps it understated — closest to how you like to look."),
  gym=dict(typed="should I go to the gym today or not…", understood="Here's what I think you're asking", q="Should I go to the gym today?",
       know="What I know about you", knowText="identity.md: aiming for three workouts a week, two done so far · soul.md: values consistency over intensity",
       confirm="Confirm and get the answer", answer="Leaning yes", conf="confidence 10%", probs=[("Yes",55),("No",45)],
       low="Not sure — this one is close to a coin flip.", why="Probability of yes: 55%. Two of three sessions done; nothing in what you said tips it.",
       reask="Ask again with this", extra="I'm travelling the next three days", answer2="Yes — go today", conf2="confidence 76%", probs2=[("Yes",88),("No",12)],
       why2="Probability of yes: 88%. Today is the last chance for the third session this week."), camTitle="Take a photo", camHint="Frame the menu", menuTitle="TODAY'S MENU", menuPlace="Corner Diner · Breakfast & Lunch", know="What I know about you", knowText="identity.md: cutting weight, no beef, prefers light meals · soul.md: would rather eat less than eat fried food", saw="What I picked up", sawText="Handwritten menu board, cream background, dark-brown lettering. Four mains: beef noodles $180 (braised broth, comes with a soy egg), chicken rice $120 (Chiayi style, chicken oil over rice), salad $150 (lettuce, cherry tomatoes, boiled egg, vinaigrette), curry pork chop $200 (deep-fried cutlet, Japanese curry). Note bottom-right: free extra rice. You said you're cutting weight and want something light today.", pick="Choose a photo", pickHint="Menus, products, outfits", understanding="Understanding…", deciding="Deciding…", listening="Listening…", typed="what should I eat today…", cap="Release to finish",
            understood="Here's what I think you're asking", q="Which dish on this menu should I have today?",
            opts=[("Beef noodles","$180 · rich broth"),("Chicken rice","$120 · lean protein"),("Salad","$150 · light, high fibre"),("Curry pork chop","$200 · fried"),("None of these","")],
            doomed=3, confirm="Confirm and get the answer", answer="Salad", conf="confidence 92%",
            probs=[("Salad",92),("Chicken rice",6),("Beef noodles",2),("None of these",0)],
            why="You're cutting weight and prefer light food — the salad fits best."),
 ),
 "zh": dict(
  lang="zh-Hant", path="/zh/", title="幫我做決定 — WDYT：說出來、確認、決定",
  desc="WDYT 把一個模糊的念頭——講幾句話、拍張菜單——變成一個你可以確認、修改的問題與選項，然後給你一個帶信心度的決定。",
  nav=["特色", "怎麼用", "常見問題"], nav_ids=["features", "how", "faq"],
  h1='你不必先想清楚要問什麼。<br><em>說出來</em>就好。',
  sub="按住按鈕，含糊地講你在猶豫什麼，有菜單就拍一張。WDYT 幫你整理出真正的問題和選項，先給你看、讓你改，確認之後才給答案——而且附上它有多確定的數字。",
  badge="iPhone · 即將上架 App Store", shots=("shot-zh.jpg", "shot-en.jpg", "shot-cn.jpg"),
  features_title="哪裡不一樣",
  features=[("開口說，不用打字", "按住或點一下麥克風說話。英文走 Apple 辨識，中文用手機上跑的 SenseVoice。語音永遠不會離開裝置。"),
            ("問題它幫你寫", "生成模型讀你的話和照片，寫出問題、選項、還有「它看到了什麼」——你從頭到尾不用填表。"),
            ("決定權在你", "沒看過之前什麼都不會決定。改問題、刪選項、加它漏掉的、修正它從照片讀錯的。然後才確認。"),
            ("給決定，不給作文", "答案來自 TypeSafe 的 Jev——一個回傳帶校準機率的選擇、而不是一段文字的模型，半秒內完成。"),
            ("不確定就老實說", "五五波就說五五波。你什麼線索都沒給，它也會說，並讓你補一句再問一次。"),
            ("你允許的話，它會越來越懂你", "兩個純文字檔——identity.md 和 soul.md——記你是誰、你怎麼做決定。預設關閉；開啟後每次回答完會修訂，你隨時可以改。")],
  how_title="三步，每步一下", how_sub="理解 → 確認 → 決定。決策模型只在你確認之後才被呼叫。",
  steps=[("說出來（拍下來）", "「我今天吃什麼……」加一張菜單照片。最多三張，送出前先在手機上縮圖。"),
         ("看它理解對不對", "一句話的問題、每個選項一行說明、還有從照片整理出的「我看到的」。有錯就改。這時什麼都還沒決定。"),
         ("確認、拿答案", "一個選擇、每個選項的機率、一個信心數字、一句為什麼。漏了什麼就補一句再問。")],
  verdicts=[("ok", "92%——很清楚", "偏好和選項對得上，就它了。"), ("close", "55%——五五波", "老實告訴你是五五波，不裝篤定。"), ("no", "資訊不足", "它會說，並請你多給一句。")],
  privacy_h="你的金鑰、你的手機。沒有 WDYT 伺服器。",
  privacy_p=f'WDYT 沒有後端。語音在裝置上辨識。理解問題是你的手機用你自己的 API 金鑰直連 Google Gemini；做決定是直連 OpenRouter（TypeSafe Jev），也是你自己的金鑰。金鑰存在 iOS Keychain。<a href="/privacy/">隱私政策</a> · <a href="/terms/">使用條款</a>',
  disclaim_b="拿來玩的，不是拿來決定人生的。",
  disclaim_p="本 App 僅供娛樂用途。所有回答由 AI 模型產生，可能出錯。重要的決定——健康、金錢、法律、安全、感情、工作——請務必諮詢專業人士評估，並用自己的判斷。使用風險自負；本 App 及其開發者不對你據此做出的任何決定負責，亦不對任何決定所造成的任何損失或損害負責。",
  faq_title="常見問題",
  faq=[("為什麼要兩把 API 金鑰？", "因為是兩件事。Gemini（Google）負責讀你的話和照片、寫出問題——要一把 Google AI Studio 的 Gemini 金鑰。Jev（TypeSafe）負責做決定——透過 OpenRouter 呼叫，所以要一把 OpenRouter 金鑰。兩邊都是你自己帳戶按量計費，一題通常遠低於一美分。WDYT 看不到任何一把金鑰。"),
       ("Jev 是什麼？為什麼不直接讓 Gemini 決定？", "Jev 是 TypeSafe 的「System One」模型：它不產生文字，只回傳有型別的答案——從你的清單選一個、一個是／否的機率、或量表上的一個位置——並附校準過的機率，大約 100–500 毫秒。信心數字之所以有意義、答案之所以瞬間出來，就是因為它。Gemini 負責 Jev 做不到的那半：聽懂模糊的話、看照片。"),
       ("決策模型看得到我的照片嗎？", "看不到——Jev 只收文字。Gemini 會把它看到的全部寫下來（菜單每一項和價格、衣服長什麼樣），Jev 判斷的就是這段文字。這段文字在確認畫面就叫「我看到的」，你可以改。"),
       ("支援哪些語言？", "介面可選 English、繁體中文、简体中文，跟手機語言無關。語音：英文用 Apple；中文用 SenseVoice，第一次要下載約 230 MB。這個模型和你手機上其他 tautiu.dev 的 App 共用，下載一次就好。"),
       ("identity.md 和 soul.md 是什麼？", "identity.md 是你是誰——飲食、預算、習慣。soul.md 是你怎麼做決定——在意什麼、避免什麼。每次提問都會一起送出，讓答案貼近你。可以自己寫，也可以開啟「允許自動更新關於我的資訊」讓 Gemini 每次回答完幫你修訂。預設關閉。"),
       ("有東西被儲存或分享嗎？", "全部留在你手機上：金鑰在 Keychain、兩個檔案、歷史紀錄。唯二的網路連線是你自己發起的那兩次，從你的手機直接到 Google 和 OpenRouter，受它們各自的隱私政策規範。")],
  cta_h="午餐別再想三十分鐘了。", cta="即將上架 App Store",
  footer_privacy="隱私政策", footer_terms="使用條款", footer_support="支援",
  demo=dict(title="幫我做決定", storyTabs=["菜單","穿搭","健身房"],
  outfit=dict(pick="加照片", pickHint="最多三張", garments=[("深藍西裝外套","navy"),("米色針織","beige"),("黑色洋裝","black")],
       typed="明天面試穿哪一套……", understood="我理解你想問的是", q="明天面試我應該穿哪一套？",
       opts=[("深藍西裝外套","正式、俐落"),("米色針織","柔和、親切"),("黑色洋裝","優雅、簡單"),("都不適合","")], doomed=None,
       saw="我看到的", sawText="床上三張照片：深藍單排扣西裝外套配白襯衫，合身版型；米色寬鬆羅紋針織衫；黑色及膝合身洋裝。你說面試地點是設計工作室。",
       know="我知道的", knowText="identity.md：產品設計師 · soul.md：寧可低調也不要過度打扮",
       confirm="確認並取得結果", answer="深藍西裝外套", conf="信心 78%", probs=[("深藍西裝外套",78),("黑色洋裝",15),("米色針織",7),("都不適合",0)],
       why="第一次見面夠正式，襯衫加外套又不會太隆重——最接近你喜歡的樣子。"),
  gym=dict(typed="我今天到底要不要去健身房……", understood="我理解你想問的是", q="我今天應該去健身房嗎？",
       know="我知道的", knowText="identity.md：目標每週運動三次，這週已做兩次 · soul.md：重視持續勝過強度",
       confirm="確認並取得結果", answer="傾向：是", conf="信心 10%", probs=[("是",55),("否",45)],
       low="不太確定——這題接近五五波。", why="「是」的機率 55%。三次做了兩次，你說的話裡沒有什麼能推向任一邊。",
       reask="帶這句再問一次", extra="接下來三天要出差", answer2="是——今天去", conf2="信心 76%", probs2=[("是",88),("否",12)],
       why2="「是」的機率 88%。今天是這週補上第三次的最後機會。"), camTitle="拍照", camHint="對準菜單", menuTitle="今日菜單", menuPlace="巷口小館 · 早午餐", know="我知道的", knowText="identity.md：減脂中、不吃牛、偏好清淡 · soul.md：寧可少吃也不吃炸的", saw="我看到的", sawText="手寫菜單板，米白底、深棕字。四道主餐：牛肉麵 $180（紅燒湯頭、附滷蛋）、雞肉飯 $120（嘉義式、雞油淋飯）、沙拉 $150（生菜、小番茄、水煮蛋、油醋醬）、咖哩豬排 $200（炸豬排、日式咖哩）。右下角註明「加飯免費」。你說在減脂、今天想吃清淡。", pick="選一張照片", pickHint="菜單、商品、穿搭都行", understanding="理解中…", deciding="決定中…", listening="聽著呢…", typed="我今天應該吃什麼……", cap="放開結束",
            understood="我理解你想問的是", q="我今天應該吃菜單上的哪一道？",
            opts=[("牛肉麵","$180 · 重口味"),("雞肉飯","$120 · 蛋白質"),("沙拉","$150 · 清淡高纖"),("咖哩豬排","$200 · 炸物"),("都不適合","")],
            doomed=3, confirm="確認並取得結果", answer="沙拉", conf="信心 92%",
            probs=[("沙拉",92),("雞肉飯",6),("牛肉麵",2),("都不適合",0)],
            why="你在減脂、偏好清淡，沙拉最符合。"),
 ),
 "cn": dict(
  lang="zh-Hans", path="/cn/", title="帮我拿主意 — WDYT：说出来、确认、决定",
  desc="WDYT 把一个模糊的念头——说几句话、拍张菜单——变成一个你可以确认、修改的问题和选项，然后给你一个带信心度的决定。",
  nav=["特色", "怎么用", "常见问题"], nav_ids=["features", "how", "faq"],
  h1='你不必先想清楚要问什么。<br><em>说出来</em>就好。',
  sub="按住按钮，含糊地说你在犹豫什么，有菜单就拍一张。WDYT 帮你整理出真正的问题和选项，先给你看、让你改，确认之后才给答案——而且附上它有多确定的数字。",
  badge="iPhone · 即将上架 App Store", shots=("shot-cn.jpg", "shot-zh.jpg", "shot-en.jpg"),
  features_title="哪里不一样",
  features=[("开口说，不用打字", "按住或点一下麦克风说话。英文走 Apple 识别，中文用手机上跑的 SenseVoice。语音永远不会离开设备。"),
            ("问题它帮你写", "生成模型读你的话和照片，写出问题、选项、还有「它看到了什么」——你从头到尾不用填表。"),
            ("决定权在你", "没看过之前什么都不会决定。改问题、删选项、加它漏掉的、修正它从照片读错的。然后才确认。"),
            ("给决定，不给作文", "答案来自 TypeSafe 的 Jev——一个返回带校准概率的选择、而不是一段文字的模型，半秒内完成。"),
            ("不确定就老实说", "五五开就说五五开。你什么线索都没给，它也会说，并让你补一句再问一次。"),
            ("你允许的话，它会越来越懂你", "两个纯文本文件——identity.md 和 soul.md——记你是谁、你怎么做决定。默认关闭；开启后每次回答完会修订，你随时可以改。")],
  how_title="三步，每步一下", how_sub="理解 → 确认 → 决定。决策模型只在你确认之后才被调用。",
  steps=[("说出来（拍下来）", "「我今天吃什么……」加一张菜单照片。最多三张，发送前先在手机上缩图。"),
         ("看它理解对不对", "一句话的问题、每个选项一行说明、还有从照片整理出的「我看到的」。有错就改。这时什么都还没决定。"),
         ("确认、拿答案", "一个选择、每个选项的概率、一个信心数字、一句为什么。漏了什么就补一句再问。")],
  verdicts=[("ok", "92%——很清楚", "偏好和选项对得上，就它了。"), ("close", "55%——五五开", "老实告诉你是五五开，不装笃定。"), ("no", "信息不足", "它会说，并请你多给一句。")],
  privacy_h="你的密钥、你的手机。没有 WDYT 服务器。",
  privacy_p=f'WDYT 没有后端。语音在设备上识别。理解问题是你的手机用你自己的 API 密钥直连 Google Gemini；做决定是直连 OpenRouter（TypeSafe Jev），也是你自己的密钥。密钥存在 iOS Keychain。<a href="/privacy/">隐私政策</a> · <a href="/terms/">使用条款</a>',
  disclaim_b="拿来玩的，不是拿来决定人生的。",
  disclaim_p="本 App 仅供娱乐用途。所有回答由 AI 模型生成，可能出错。重要的决定——健康、金钱、法律、安全、感情、工作——请务必咨询专业人士评估，并用自己的判断。使用风险自负；本 App 及其开发者不对你据此做出的任何决定负责，亦不对任何决定所造成的任何损失或损害负责。",
  faq_title="常见问题",
  faq=[("为什么要两把 API 密钥？", "因为是两件事。Gemini（Google）负责读你的话和照片、写出问题——要一把 Google AI Studio 的 Gemini 密钥。Jev（TypeSafe）负责做决定——通过 OpenRouter 调用，所以要一把 OpenRouter 密钥。两边都是你自己账户按量计费，一题通常远低于一美分。WDYT 看不到任何一把密钥。"),
       ("Jev 是什么？为什么不直接让 Gemini 决定？", "Jev 是 TypeSafe 的「System One」模型：它不生成文字，只返回有类型的答案——从你的清单选一个、一个是／否的概率、或量表上的一个位置——并附校准过的概率，大约 100–500 毫秒。信心数字之所以有意义、答案之所以瞬间出来，就是因为它。Gemini 负责 Jev 做不到的那半：听懂模糊的话、看照片。"),
       ("决策模型看得到我的照片吗？", "看不到——Jev 只收文字。Gemini 会把它看到的全部写下来（菜单每一项和价格、衣服长什么样），Jev 判断的就是这段文字。这段文字在确认页面就叫「我看到的」，你可以改。"),
       ("支持哪些语言？", "界面可选 English、繁體中文、简体中文，跟手机语言无关。语音：英文用 Apple；中文用 SenseVoice，第一次要下载约 230 MB。这个模型和你手机上其他 tautiu.dev 的 App 共用，下载一次就好。"),
       ("identity.md 和 soul.md 是什么？", "identity.md 是你是谁——饮食、预算、习惯。soul.md 是你怎么做决定——在意什么、避免什么。每次提问都会一起发送，让答案贴近你。可以自己写，也可以开启「允许自动更新关于我的信息」让 Gemini 每次回答完帮你修订。默认关闭。"),
       ("有东西被存储或分享吗？", "全部留在你手机上：密钥在 Keychain、两个文件、历史记录。仅有的网络连接是你自己发起的那两次，从你的手机直接到 Google 和 OpenRouter，受它们各自的隐私政策约束。")],
  cta_h="午餐别再想三十分钟了。", cta="即将上架 App Store",
  footer_privacy="隐私政策", footer_terms="使用条款", footer_support="支持",
  demo=dict(title="帮我拿主意", storyTabs=["菜单","穿搭","健身房"],
  outfit=dict(pick="加照片", pickHint="最多三张", garments=[("深蓝西装外套","navy"),("米色针织","beige"),("黑色连衣裙","black")],
       typed="明天面试穿哪一套……", understood="我理解你想问的是", q="明天面试我应该穿哪一套？",
       opts=[("深蓝西装外套","正式、利落"),("米色针织","柔和、亲切"),("黑色连衣裙","优雅、简单"),("都不合适","")], doomed=None,
       saw="我看到的", sawText="床上三张照片：深蓝单排扣西装外套配白衬衫，合身版型；米色宽松罗纹针织衫；黑色及膝合身连衣裙。你说面试地点是设计工作室。",
       know="我知道的", knowText="identity.md：产品设计师 · soul.md：宁可低调也不要过度打扮",
       confirm="确认并获取结果", answer="深蓝西装外套", conf="信心 78%", probs=[("深蓝西装外套",78),("黑色连衣裙",15),("米色针织",7),("都不合适",0)],
       why="第一次见面够正式，衬衫加外套又不会太隆重——最接近你喜欢的样子。"),
  gym=dict(typed="我今天到底要不要去健身房……", understood="我理解你想问的是", q="我今天应该去健身房吗？",
       know="我知道的", knowText="identity.md：目标每周运动三次，这周已做两次 · soul.md：重视持续胜过强度",
       confirm="确认并获取结果", answer="倾向：是", conf="信心 10%", probs=[("是",55),("否",45)],
       low="不太确定——这题接近五五开。", why="「是」的概率 55%。三次做了两次，你说的话里没有什么能推向任一边。",
       reask="带这句再问一次", extra="接下来三天要出差", answer2="是——今天去", conf2="信心 76%", probs2=[("是",88),("否",12)],
       why2="「是」的概率 88%。今天是这周补上第三次的最后机会。"), camTitle="拍照", camHint="对准菜单", menuTitle="今日菜单", menuPlace="巷口小馆 · 早午餐", know="我知道的", knowText="identity.md：减脂中、不吃牛、偏好清淡 · soul.md：宁可少吃也不吃炸的", saw="我看到的", sawText="手写菜单板，米白底、深棕字。四道主餐：牛肉面 $180（红烧汤头、附卤蛋）、鸡肉饭 $120（嘉义式、鸡油淋饭）、沙拉 $150（生菜、小番茄、水煮蛋、油醋汁）、咖喱猪排 $200（炸猪排、日式咖喱）。右下角注明「加饭免费」。你说在减脂、今天想吃清淡。", pick="选一张照片", pickHint="菜单、商品、穿搭都行", understanding="理解中…", deciding="决定中…", listening="听着呢…", typed="我今天应该吃什么……", cap="松开结束",
            understood="我理解你想问的是", q="我今天应该吃菜单上的哪一道？",
            opts=[("牛肉面","$180 · 重口味"),("鸡肉饭","$120 · 蛋白质"),("沙拉","$150 · 清淡高纤"),("咖喱猪排","$200 · 炸物"),("都不合适","")],
            doomed=3, confirm="确认并获取结果", answer="沙拉", conf="信心 92%",
            probs=[("沙拉",92),("鸡肉饭",6),("牛肉面",2),("都不合适",0)],
            why="你在减脂、偏好清淡，沙拉最符合。"),
 ),
}

LANG_SWITCH = [("en", "/", "English"), ("zh", "/zh/", "繁體中文"), ("cn", "/cn/", "简体中文")]


def head(t, url, extra_meta=""):
    alts = "".join(f'<link rel="alternate" hreflang="{T[k]["lang"]}" href="{SITE}{T[k]["path"]}">' for k in T)
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['title'])}</title>
<meta name="description" content="{html.escape(t['desc'])}">
<meta property="og:title" content="WDYT"><meta property="og:description" content="{html.escape(t['desc'])}">
<meta property="og:image" content="{SITE}/og.png"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{alts}<link rel="alternate" hreflang="x-default" href="{SITE}/">
<link rel="icon" type="image/png" href="/icon.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
{extra_meta}<style>{CSS}</style>
</head>"""


def nav(t, key):
    links = "".join(f'<a href="#{i}">{html.escape(n)}</a>' for n, i in zip(t["nav"], t["nav_ids"]))
    lang = " · ".join(f'<a href="{p}" class="{"active" if k == key else ""}">{lbl}</a>' for k, p, lbl in LANG_SWITCH)
    return f"""<nav><a class="brand" href="{t['path']}"><img src="/icon.png" alt="">WDYT</a>
<div class="links">{links}<span class="lang">{lang}</span></div></nav>"""


MIC_SVG = '<svg viewBox="0 0 24 24"><path d="M12 15a4 4 0 0 0 4-4V6a4 4 0 1 0-8 0v5a4 4 0 0 0 4 4zm6-4a6 6 0 0 1-5 5.92V20h3v2H8v-2h3v-3.08A6 6 0 0 1 6 11h2a4 4 0 0 0 8 0h2z"/></svg>'


def _bar(title, back=False):
    left = '<small>‹</small>' if back else ''
    return f'<div class="bar">{left}{html.escape(title)}<small>{"" if back else "⚙"}</small></div>'

def _opts(opts, doomed):
    return "".join(f'<div class="opt{" doomed" if i == doomed else ""}"><span>{html.escape(l)}<br><small>{html.escape(sub)}</small></span><span class="x">×</span></div>' for i, (l, sub) in enumerate(opts))

def _probs(probs):
    return "".join(f'<div class="prob"><span>{html.escape(l)}</span><i style="--w:{p}%"></i><b>{p}%</b></div>' for l, p in probs)

def _talk(d, title, typed, thumb_html, listening, cap, understanding):
    return f"""<div class="scene s1">
  {_bar(title)}
  <div class="card">{thumb_html}<span class="muted">{html.escape(listening)}</span><div class="typed" data-text="{html.escape(typed)}"></div></div>
  <div class="mic">{MIC_SVG}</div><div class="cap">{html.escape(cap)}</div>
  <div class="busy b1"><i></i>{html.escape(understanding)}</div>
 </div>"""

def _confirm(understood, q, opts_html, saw, sawText, know, knowText, confirm, deciding):
    saw_html = f'<div class="card saw"><div class="muted">{html.escape(saw)}</div><div class="sawtext">{html.escape(sawText)}</div></div>' if saw else ''
    return f"""<div class="scene s2">
  {_bar(understood, back=True)}
  <div class="card"><div class="muted">Q</div><div style="font-weight:600">{html.escape(q)}</div></div>
  {('<div class="card">' + opts_html + '</div>') if opts_html else ''}
  {saw_html}
  <div class="card saw know"><div class="muted">{html.escape(know)}</div><div class="sawtext">{html.escape(knowText)}</div></div>
  <div class="btn">{html.escape(confirm)}</div>
  <div class="busy b2"><i></i>{html.escape(deciding)}</div>
 </div>"""

def _result(q, answer, conf, probs, why, low=None, low_cls="", reask=None, extra=None, cls="s3"):
    banner = f'<div class="lowc">{html.escape(low)}</div>' if low else ''
    re = f'<div class="reask"><div class="field"><span class="typed2" data-text="{html.escape(extra)}"></span><span class="mmic">{MIC_SVG}</span></div><div class="btn ghost">{html.escape(reask)}</div></div>' if reask else ''
    return f"""<div class="scene {cls}{" low" if low else ""}">
  {_bar("", back=True)}
  <div class="muted" style="margin-top:.8em">{html.escape(q)}</div>
  <div class="card"><div class="big">{html.escape(answer)}</div><div class="conf {low_cls}">{"?" if low else "✓"} {html.escape(conf)}</div></div>
  {banner}
  <div class="card">{_probs(probs)}</div>
  <div class="why">{html.escape(why)}</div>
  {re}
 </div>"""

def story_menu(d):
    menu_rows = "".join(f'<div class="mrow"><span>{html.escape(l)}</span><span class="dots"></span><span>{html.escape(sub.split(" · ")[0])}</span></div>' for l, sub in d["opts"] if sub)
    mini = f'<span class="board mini"><div class="mtitle">{html.escape(d["menuTitle"])}</div>{menu_rows}</span>'
    s0 = f"""<div class="scene s0 vf">
  <div class="vfbar"><span>×</span><b>{html.escape(d['camTitle'])}</b><span></span></div>
  <div class="board"><div class="place">{html.escape(d['menuPlace'])}</div><div class="mtitle">{html.escape(d['menuTitle'])}</div>{menu_rows}</div>
  <div class="corners"><i></i><i></i><i></i><i></i></div>
  <div class="vfhint">{html.escape(d['camHint'])}</div>
  <div class="shutter"><i></i></div><div class="flash"></div>
  <div class="captured"><div class="board mini"><div class="mtitle">{html.escape(d['menuTitle'])}</div>{menu_rows}</div></div>
 </div>"""
    scenes = s0 + _talk(d, d['title'], d['typed'], f'<span class="thumb">{mini}</span>', d['listening'], d['cap'], d['understanding']) \
        + _confirm(d['understood'], d['q'], _opts(d['opts'], d['doomed']), d['saw'], d['sawText'], d['know'], d['knowText'], d['confirm'], d['deciding']) \
        + _result(d['q'], d['answer'], d['conf'], d['probs'], d['why'])
    # timeline: [ms, op, selector, class]  op: go=k | add | rm | type
    tl = [[0,"go",0],[2000,"add",".s0","shot"],[3300,"go",1],[4200,"type",".s1 .typed"],[7000,"add",".s1 .mic","idle"],[7000,"add",".b1","on"],
          [8200,"go",2],[10100,"add",".s2 .doomed","gone"],[11300,"add",".s2 .btn","press"],[11600,"add",".b2","on"],[12400,"go",3],[17800,"end"]]
    return scenes, tl, 4

def story_outfit(d, o):
    tiles = "".join(f'<div class="gtile {c}"><div class="garment {c}"></div><div class="gl">{html.escape(n)}</div><div class="chk">✓</div></div>' for n, c in o["garments"])
    s0 = f"""<div class="scene s0">
  {_bar(d['title'])}
  <div class="sheet"><div class="hd">{html.escape(o['pick'])}<small>✓</small></div><div class="muted">{html.escape(o['pickHint'])}</div>
   <div class="grid g3">{tiles}</div></div>
 </div>"""
    thumbs = '<span class="thumbs">' + "".join(f'<span class="thumb tiny"><span class="garment {c}"></span></span>' for _, c in o["garments"]) + '</span>'
    scenes = s0 + _talk(d, d['title'], o['typed'], thumbs, d['listening'], d['cap'], d['understanding']) \
        + _confirm(o['understood'], o['q'], _opts(o['opts'], o['doomed']), o['saw'], o['sawText'], o['know'], o['knowText'], o['confirm'], d['deciding']) \
        + _result(o['q'], o['answer'], o['conf'], o['probs'], o['why'])
    tl = [[0,"go",0],[700,"add",".s0 .gtile:nth-child(1)","sel"],[1300,"add",".s0 .gtile:nth-child(2)","sel"],[1900,"add",".s0 .gtile:nth-child(3)","sel"],
          [2900,"go",1],[3700,"type",".s1 .typed"],[6800,"add",".s1 .mic","idle"],[6800,"add",".b1","on"],[8000,"go",2],
          [10600,"add",".s2 .btn","press"],[10900,"add",".b2","on"],[11700,"go",3],[17000,"end"]]
    return scenes, tl, 4

def story_gym(d, g):
    scenes = _talk(d, d['title'], g['typed'], '', d['listening'], d['cap'], d['understanding']) \
        + _confirm(g['understood'], g['q'], '', None, None, g['know'], g['knowText'], g['confirm'], d['deciding']) \
        + _result(g['q'], g['answer'], g['conf'], g['probs'], g['why'], low=g['low'], low_cls="lowconf", reask=g['reask'], extra=g['extra']) \
        + _result(g['q'], g['answer2'], g['conf2'], g['probs2'], g['why2'], cls="s4")
    tl = [[0,"go",0],[800,"type",".s1 .typed"],[4000,"add",".s1 .mic","idle"],[4000,"add",".b1","on"],[5200,"go",1],
          [7400,"add",".s2 .btn","press"],[7700,"add",".b2","on"],[8500,"go",2],[11000,"type",".s3 .typed2"],[13600,"add",".s3 .ghost","press"],
          [14200,"go",3],[19000,"end"]]
    return scenes, tl, 4

def demo(d):
    """Hero animation: three stories (menu → outfit → gym), each a phone walking through
    record → understand/edit → decide; story tabs above; auto-advances; reduced-motion shows results."""
    import json as _json
    built = [story_menu(d), story_outfit(d, d['outfit']), story_gym(d, d['gym'])]
    phones = ""
    tls = []
    for i, (scenes, tl, n) in enumerate(built):
        dots = "".join(f'<i class="{"on" if k == 0 else ""}"></i>' for k in range(n))
        phones += f'<div class="story{" on" if i == 0 else ""}" data-story="{i}">{scenes}<div class="dots">{dots}</div></div>'
        tls.append(tl)
    tabs = "".join(f'<button class="{"on" if i == 0 else ""}" data-tab="{i}">{html.escape(t)}</button>' for i, t in enumerate(d['storyTabs']))
    return f"""<div class="demo-wrap"><div class="tabs" id="demotabs">{tabs}</div>
<div class="demo" id="demo" aria-label="WDYT demo"><div class="screen">{phones}</div></div></div>
<script>(function(){{var TL={_json.dumps(tls)};var wrap=document.getElementById("demo");if(!wrap)return;var stories=wrap.querySelectorAll(".story"),tabs=document.querySelectorAll("#demotabs button");var rm=matchMedia("(prefers-reduced-motion: reduce)").matches;var cur=0,T=[];
function scenes(st){{return st.querySelectorAll(".scene")}}function go(st,k){{scenes(st).forEach(function(s,i){{s.classList.toggle("on",i===k)}});st.querySelectorAll(".dots i").forEach(function(d,i){{d.classList.toggle("on",i===k)}})}}
function reset(st){{st.querySelectorAll(".typed,.typed2").forEach(function(e){{e.textContent=""}});st.querySelectorAll(".gone,.press,.shot,.idle,.sel").forEach(function(e){{e.classList.remove("gone","press","shot","idle","sel")}});st.querySelectorAll(".busy.on").forEach(function(e){{e.classList.remove("on")}})}}
function typeInto(el){{var t=el.getAttribute("data-text"),i=0;el.textContent="";(function step(){{if(i<t.length){{el.textContent+=t[i++];T.push(setTimeout(step,85))}}}})()}}
function show(idx){{T.forEach(clearTimeout);T=[];cur=idx;stories.forEach(function(s,i){{s.classList.toggle("on",i===idx)}});tabs.forEach(function(b,i){{b.classList.toggle("on",i===idx)}});var st=stories[idx];reset(st);if(rm){{st.querySelectorAll(".typed,.typed2").forEach(function(e){{e.textContent=e.getAttribute("data-text")}});go(st,scenes(st).length-1);return}}
TL[idx].forEach(function(step){{T.push(setTimeout(function(){{var op=step[1];if(op==="go")go(st,step[2]);else if(op==="add"){{var e=st.querySelector(step[2]);if(e)e.classList.add(step[3])}}else if(op==="type"){{var e2=st.querySelector(step[2]);if(e2)typeInto(e2)}}else if(op==="end")show((idx+1)%stories.length)}},step[0]))}})}}
tabs.forEach(function(b){{b.addEventListener("click",function(){{show(+b.getAttribute("data-tab"))}})}});var q=+(new URLSearchParams(location.search).get("story")||0);show(isNaN(q)?0:Math.max(0,Math.min(stories.length-1,q)))}})();</script>"""


def cta_link(t):
    if STORE_URL:
        return f'<a class="cta" href="{STORE_URL}">{html.escape(t["cta"])}</a>'
    return f'<span class="cta pending">{html.escape(t["cta"])}</span>'


def landing(key):
    t = T[key]
    icons = ["🎤", "✎", "☑", "⚡", "½", "✦"]
    feats = "".join(f'<div class="feature"><div class="icon">{icons[i]}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for i, (h, p) in enumerate(t["features"]))
    steps = "".join(f'<div class="step"><div class="num">{i+1}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for i, (h, p) in enumerate(t["steps"]))
    verdicts = "".join(f'<div class="verdict {c}"><b>{html.escape(l)}</b>{html.escape(p)}</div>' for c, l, p in t["verdicts"])
    faq = "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in t["faq"])
    badge = f'<a class="badge" href="{STORE_URL}">{html.escape(t["badge"])}</a>' if STORE_URL else f'<span class="badge">{html.escape(t["badge"])}</span>'
    redirect = ""
    if key == "en":
        redirect = """<script>(function(){var p=new URLSearchParams(location.search);if(p.get("lang")==="en")return;var s=null;try{s=localStorage.getItem("wdyt-lang")}catch(e){}if(s){if(s!=="/")location.replace(s);return}var L=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||""];for(var i=0;i<L.length;i++){var l=L[i].toLowerCase();if(/^zh-(hans|cn|sg)/.test(l)){location.replace("/cn/");return}if(/^zh/.test(l)){location.replace("/zh/");return}if(/^en/.test(l))return}})();</script>"""
    remember = """<script>document.addEventListener("click",function(e){var a=e.target.closest(".lang a");if(!a)return;try{localStorage.setItem("wdyt-lang",a.getAttribute("href"))}catch(e){}});</script>"""
    return f"""{head(t, SITE + t['path'], redirect + remember)}
<body>
{nav(t, key)}
<header class="hero">
  <h1>{t['h1']}</h1>
  <p class="sub">{html.escape(t['sub'])}</p>
  {badge}
  {demo(t['demo'])}
</header>
<section class="features" id="features">
  <h2 class="section-title">{html.escape(t['features_title'])}</h2>
  <div class="features-grid">{feats}</div>
</section>
<section class="how" id="how">
  <h2 class="section-title">{html.escape(t['how_title'])}</h2>
  <p class="section-sub">{html.escape(t['how_sub'])}</p>
  <div class="steps">{steps}</div>
</section>
<div class="verdicts">{verdicts}</div>
<section class="privacy"><div class="privacy-card"><h2>{html.escape(t['privacy_h'])}</h2><p>{t['privacy_p']}</p></div></section>
<section class="disclaim"><div class="card"><b>{html.escape(t['disclaim_b'])}</b>{html.escape(t['disclaim_p'])}</div></section>
<section class="faq" id="faq"><h2 class="section-title">{html.escape(t['faq_title'])}</h2><div class="faq">{faq}</div></section>
<div class="bottom-cta"><h2>{html.escape(t['cta_h'])}</h2>{cta_link(t)}</div>
<footer>© 2026 WDYT · tautiu.dev · <a href="/privacy/">{t['footer_privacy']}</a> · <a href="/terms/">{t['footer_terms']}</a> · <a href="/support/">{t['footer_support']}</a> · <a href="mailto:{MAIL}">{MAIL}</a></footer>
</body></html>
"""


def legal(slug, title, desc, body_html):
    t = dict(T["en"], title=f"{title} — WDYT", desc=desc)
    return f"""{head(t, f"{SITE}/{slug}/")}
<body>
<main class="legal">
  <a class="home" href="/">← WDYT</a>
  <h1>{title}</h1>
  <div class="updated">Last updated: {LAST_UPDATED} · Applies to WDYT for iOS</div>
{body_html}
  <footer style="margin-top:3rem">© 2026 WDYT · tautiu.dev · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/support/">Support</a></footer>
</main>
</body></html>
"""


PRIVACY = f"""
  <div class="card"><p><strong>The short version:</strong> WDYT has no servers and no accounts. Speech is recognised on your device. The only network calls are the two you initiate — understanding your question with Google Gemini, and deciding with TypeSafe Jev via OpenRouter — and both go straight from your phone to that provider, with your own API keys.</p></div>

  <h2>What we collect</h2>
  <p>Nothing that identifies you. WDYT has no accounts, no analytics SDKs, no advertising, and no third-party trackers. We operate no server that your device talks to.</p>

  <h2>Microphone and speech recognition</h2>
  <p>When you record, your speech is transcribed on the device: English with Apple's Speech framework (depending on your device and iOS settings Apple may process speech on its servers under <a href="https://www.apple.com/legal/privacy/">Apple's privacy policy</a>), Mandarin with the SenseVoice model running locally via sherpa-onnx. WDYT does not store audio; the transcript exists only for the current question and you can edit it before anything is sent.</p>

  <h2>Photos</h2>
  <p>Photos you attach are resized on the device (longest edge 1280 px) and sent only to Google Gemini as part of understanding your question, using your own key. They are never sent to the decision model or anywhere else, and are discarded when you start a new question. WDYT does not access your photo library beyond the pictures you pick.</p>

  <h2>Your API keys and the two providers</h2>
  <p>WDYT works with two keys you paste in Settings. Your <strong>Gemini API key</strong> is used to send your transcribed words, your photos and your profile (see below) directly to Google under <a href="https://policies.google.com/privacy">Google's privacy policy</a>. Your <strong>OpenRouter API key</strong> is used to send the confirmed question, options and profile directly to OpenRouter, which routes it to TypeSafe's Jev model, under <a href="https://openrouter.ai/privacy">OpenRouter's</a> and <a href="https://docs.typesafe.ai/legal">TypeSafe's</a> policies. Keys are stored in your device's Keychain, never leave the device except to the provider they belong to, and are removed when you clear the field or delete the app. WDYT never receives your keys or your content.</p>

  <h2>Your profile: identity.md and soul.md</h2>
  <p>Two plain-text files on your device describe your preferences and how you decide. You can write, edit or clear them in Settings at any time. They are included in the requests above so answers fit you. If you turn on <em>update these from my questions</em> (off by default), after each answer your question and edits are sent to Gemini with your key, which returns revised files; nothing else is stored, and the setting can be turned off at any time.</p>

  <h2>Data stored on your device</h2>
  <p>Settings, the two profile files, your recent decisions and the downloaded SenseVoice model live on your device. The SenseVoice model is stored in a shared container so other apps from the same developer (tautiu.dev) can use the same copy. Deleting the app removes its data; the shared model remains until the last app using it is removed.</p>

  <h2>Children</h2>
  <p>WDYT is intended for users aged 13 and up and does not knowingly collect data from children. It collects no personal data from anyone.</p>

  <h2>Changes</h2>
  <p>If this policy changes, the new version is published at this address with a new date, and material changes are noted in the app's release notes.</p>

  <h2>Contact</h2>
  <p><a href="mailto:{MAIL}">{MAIL}</a></p>
"""

TERMS = f"""
  <div class="card"><p><strong>Entertainment only.</strong> WDYT is for fun. Its answers come from AI models and can be wrong. For anything that matters — health, money, legal matters, safety, relationships, work — consult a qualified professional and use your own judgment. Never act on an irrational or harmful decision because an app suggested it. You use WDYT at your own risk. WDYT and its developer are not responsible for any decision made with it, nor for any loss or damage of any kind arising from such decisions. You confirm you have read this notice when you first open the app.</p></div>

  <h2>What WDYT is</h2>
  <p>WDYT is software that helps you phrase a question and obtain a suggestion from third-party AI models. It provides no advice of its own and no professional services of any kind.</p>

  <h2>Your own API keys</h2>
  <p>WDYT requires your own accounts with Google (Gemini) and OpenRouter (for TypeSafe Jev). Their terms, pricing and availability apply; any charges they bill are yours. WDYT is not a party to those relationships and cannot see or recover your keys.</p>

  <h2>Content and models</h2>
  <p>Questions, options and answers are generated by third-party models from your input. They may be inaccurate, incomplete or inappropriate. Confidence figures are the model's own estimate, not a guarantee. You are responsible for what you ask and what you do with the answer.</p>

  <h2>Acceptable use</h2>
  <p>Do not use WDYT to make or justify decisions that could harm you or others, to seek medical, legal or financial advice, or in any way that violates the providers' terms. Do not attempt to circumvent App Store rules.</p>

  <h2>Purchases</h2>
  <p>WDYT is currently free. If paid features are introduced, they will be sold through the App Store under Apple's terms; pricing, billing, renewal and refunds are handled by Apple.</p>

  <h2>Warranty disclaimer</h2>
  <p>WDYT is provided "as is", without warranty of any kind. Speech recognition and AI models make mistakes. We do not warrant that third-party services remain available or accurate.</p>

  <h2>Limitation of liability</h2>
  <p>To the maximum extent permitted by law, WDYT and its developer are not liable for any direct, indirect, incidental or consequential damages, or any loss of any kind, arising from use of WDYT or from any decision made with it. Our total liability for any claim is limited to the amount you paid for WDYT in the twelve months preceding the claim.</p>

  <h2>Changes and termination</h2>
  <p>We may update these terms; the current version always lives at this address, and material changes will be noted in the app's release notes. You can stop using WDYT at any time by deleting it, which removes all local data.</p>

  <h2>Contact</h2>
  <p><a href="mailto:{MAIL}">{MAIL}</a></p>
"""

SUPPORT = f"""
  <h2>Contact</h2>
  <p>Email <a href="mailto:{MAIL}">{MAIL}</a>. Include your iOS version and, if it concerns a specific answer, a screenshot of the confirm screen.</p>

  <h2>Common questions</h2>
  <p><strong>"Add your Gemini API key" / "Add your OpenRouter API key".</strong> WDYT needs both. Get a Gemini key at <a href="https://aistudio.google.com/apikey">Google AI Studio</a> (starts with "AIza") and an OpenRouter key at <a href="https://openrouter.ai/keys">openrouter.ai/keys</a> (starts with "sk-or-"). Paste each in Settings and tap Test.</p>
  <p><strong>The app didn't hear me.</strong> In hold mode, keep the button pressed for the whole sentence. In tap mode, tap once to start and again to finish. Check Settings → Privacy &amp; Security → Microphone and Speech Recognition are on for WDYT.</p>
  <p><strong>Chinese recognition is poor or asks for a download.</strong> Mandarin uses the SenseVoice model (~230 MB). Download it in Settings → Speech engine, ideally on Wi-Fi. Until then Apple's recogniser is used.</p>
  <p><strong>It misread my menu.</strong> On the confirm screen, edit "What I picked up" and the options before confirming — the decision model only ever sees that text.</p>
  <p><strong>The answer says "close to a coin flip" or "not enough to go on".</strong> That's honest output. Add one sentence about what matters (e.g. "something light") in the field under the answer and ask again; the question is re-understood with it.</p>
  <p><strong>Where are identity.md and soul.md?</strong> Settings → About you. Both are editable; the auto-update toggle is off by default.</p>
"""


def main():
    for key in T:
        out = ROOT / "index.html" if key == "en" else ROOT / T[key]["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(landing(key), encoding="utf-8")
    for slug, title, desc, body in [
        ("privacy", "Privacy Policy", "WDYT privacy policy: no servers, no accounts, on-device speech; your own API keys go straight to Google and OpenRouter.", PRIVACY),
        ("terms", "Terms of Service", "WDYT terms of service and entertainment-only disclaimer.", TERMS),
        ("support", "Support", "WDYT support: contact and common questions.", SUPPORT),
    ]:
        (ROOT / slug).mkdir(exist_ok=True)
        (ROOT / slug / "index.html").write_text(legal(slug, title, desc, body), encoding="utf-8")
    (ROOT / "CNAME").write_text("wdytai.app\n")
    print("built: index, zh, cn, privacy, terms, support")


if __name__ == "__main__":
    main()
