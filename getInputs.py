from GetUIData import *
from util import *
import datetime
from download import *

def utilInputs(form=None, util=None):
    if util=='NewsAssistant':
        selected = {'pph_1':'','pph_2':'','pph_3':'','pph_4':'','pph_5':''}
        selected[form['pf']]='selected'

        top_news = News.get_top_news(form['date'], range(1, 4), form['kw'])

        portfolio_list,portfolio_news = News.get_portfolio_news(form['date'],form['pf'],form['kw'])

        # download_data = package(form['date'],form['pf'],form['kw'])

        if portfolio_list:
            ret = Chart.get_chart_data(form['date'],form['pf'])
        else:
            ret=''
        
        top_tws = Twitter.get_top_twitter(form['date'], range(1, 5))

        celebs, hot_tws = Twitter.get_hot_twitter(form['date'])
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_days = [{'full': w, 'short': w[:3]} for w in week]

        hour = ['{:02d}'.format(i) for i in range(12)]
        minute = ['{:02d}'.format(i) for i in range(60)]

        return {
            'date': form['date'],
            'selected': selected,
            'portfolio': portfolio_list,
            'portfolio_news': portfolio_news,
            'keyword': form['kw'],
            'top_news': top_news,
            'ret': ret,
            'top_tws': top_tws,
            'hot_tws': hot_tws,
            'celebs': celebs,
            'week_days': week_days,
            'hour': hour,
            'minute': minute,
            # 'download_data':download_data
        }
    elif util == 'download':
        download_data = package(form['date'],form['pf'],form['kw'])
        return {
            'download_data':download_data
        }

    elif util=='Stock':
        return {}
    elif util == 'download':
        download_data = package(form['date'],form['pf'],form['kw'])
        return {
            'download_data':download_data
        }
    else:
        return {}


def userHistory(user):
	clicks = user.copyClicks()
	clicks.reverse()
	notes = user.copyNotes()
	notes.reverse()
	click_days, note_days = [], []
	def getCrude(news):
		return news['time'][:8]
	def getTime(news):
		time = news['time']
		return datetime(int(time[:4]), int(time[4:6]), int(time[6:8])).strftime('%b %d, %Y')
	if len(clicks)>0:
		click_days = [{'date':getTime(clicks[0]), 'crude': getCrude(clicks[0]), 'clicks':[clicks.pop(0)]}]
		for i, click in enumerate(clicks):
			time = getTime(click)
			if time==click_days[-1]['date']:
				click_days[-1]['clicks'].append(click)
			else:
				click_days.append({'date':time, 'crude':getCrude(click), 'clicks':[click]})
	if len(notes)>0:
		note_days = [{'date':getTime(notes[0]), 'crude': getCrude(notes[0]), 'notes':[notes.pop(0)]}]
		for i, note in enumerate(notes):
			time = getTime(note)
			if time==note_days[-1]['date']:
				note_days[-1]['notes'].append(note)
			else:
				note_days.append({'date':time, 'crude': getCrude(note), 'notes':[note]})
	return {
		'click': click_days,
		'note': note_days,
	}

def userLog(user):
	logs = user.copyLogs()
	logs.reverse()
	log_days = []
	def getCrude(news):
		return news['content']['time'][:8]
	def getTime(news):
		time = news['content']['time']
		return datetime(int(time[:4]), int(time[4:6]), int(time[6:8])).strftime('%b %d, %Y')
	if len(logs)>0:
		log_days = [{'date':getTime(logs[0]), 'crude': getCrude(logs[0]), 'logs':[logs.pop(0)]}]
		for i, log in enumerate(logs):
			time = getTime(log)
			if time==log_days[-1]['date']:
				log_days[-1]['logs'].append(log)
			else:
				log_days.append({'date':time, 'crude':getCrude(log), 'logs':[log]})
	return log_days








