import configparser, tkinter as tk


def set_config(rss_url, telegram_bot, tk):
	config = configparser.ConfigParser()

	config['TELEGRAM'] = {
		'bot_token': telegram_bot.get()
	}


	config['RSS'] = {
		'URL': rss_url.get()
	}

	with open('settings.ini', 'w') as configfile:
		config.write(configfile)

	tk.destroy()

input_box = tk.Tk()
frame = tk.Frame(input_box)
frame.grid(row=3, column=2)

label_rss_url = tk.Label(frame, text="RSS URL")
label_rss_url.grid(row=1, column=1, padx=4, pady=4)
entry_rss_url = tk.Entry(frame, bd=2, width=40)
entry_rss_url.grid(row=1, column=2, padx=4, pady=4)

label_telegram_bot = tk.Label(frame, text="Telegram bot token")
label_telegram_bot.grid(row=2, column=1, padx=4, pady=4)
entry_telegram_bot = tk.Entry(frame, bd=2, width=40)
entry_telegram_bot.grid(row=2, column=2, padx=4, pady=4)

done = tk.Button(frame, text='Done', command=lambda:set_config(entry_rss_url, entry_telegram_bot, input_box))
done.grid(row=3, columnspan=2, column=1, ipadx=15, pady=4)
input_box.mainloop()

