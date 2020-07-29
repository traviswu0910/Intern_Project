from GetUIData import *
from util import *

def utilInputs(form=None, util=None):
    if util=='NewsAssistant':
        selected = {'pph_1':'','pph_2':'','pph_3':'','pph_4':'','pph_5':''}
        selected[form['pf']]='selected'

        top_news = News.get_top_news(form['date'], range(1, 4), form['kw'])

        portfolio_list,portfolio_news = News.get_portfolio_news(form['date'],form['pf'],form['kw'])
        if portfolio_list:
            ret = Chart.get_chart_data(form['date'],form['pf'])
        else:
            ret=''
        
        top_tws = Twitter.get_top_twitter(form['date'], range(1, 5))

        celebs, hot_tws = Twitter.get_hot_twitter(form['date'])

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
        }
    elif util=='Stock':
        return {}
    else:
        return {}


def userHistory(user):
	return {
		'click': user.userfeed.info[user.tag]['click'],
		'note': user.userfeed.info[user.tag]['note'],
	}










