from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2015,11,1)
    end = datetime.datetime(2016,3,10)
    df = data.DataReader(name='GOOG', data_source='yahoo', start=start, end=end)
    df

    def incr_or_decr(c,o):
        if c > o:
            value = "Increase"
        if c < o:
            value = "Decrease"
        if c == o:
            value = "Equal"
        return value

    df["Status"] = [incr_or_decr(c,o) for c, o in zip(df.Close,df.Open)]
    df['Average'] = (df.Open+df.Close)/2
    hours_12 = 12*60*60*1000
    df['Height'] = abs(df.Open-df.Close)

    chart_1 = figure(x_axis_type='datetime', width=1000, height=300, 
                    sizing_mode='scale_width')
    chart_1.title.text = "Candlestick Chart"
    chart_1.grid.grid_line_alpha = 0.5

    chart_1.segment(df.index, df.High, df.index, df.Low, color="Black")

    chart_1.rect(df.index[df.Status == 'Increase'], df.Average[df.Status == 'Increase'], 
                hours_12, df.Height[df.Status == 'Increase'], fill_color = '#CCFFFF', 
                line_color='black')

    chart_1.rect(df.index[df.Status == 'Decrease'], df.Average[df.Status == 'Decrease'], 
                hours_12, df.Height[df.Status == 'Decrease'], fill_color ='#FF3333', 
                line_color='black')

    javascript_script, html_div = components(chart_1)
    cdn_js = CDN.js_files[0]
    
    return render_template("plot.html",
    javascript_script=javascript_script, 
    html_div=html_div,
    cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
