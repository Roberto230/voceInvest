from multiprocessing.sharedctypes import Value
from ntpath import join
from turtle import color
from flask import Flask, render_template, url_for, request
from script.main import Portfolio

app = Flask(__name__)

@app.route("/")
def main():
   return  render_template("index.html", home=True)

@app.route("/simple")
def simple():
    return render_template("simple.html", home=False)

@app.route("/calculate", methods=["post"])
def get_tiker():
    get_assets = request.form.getlist("assets")
    investment = request.form["totalInvestment"]
    portifolio = [i for i in get_assets if i]
    result = Portfolio.get_investiment(portifolio, investment)
    result_arr = []
    result_str = ""
    color = "alert-success"
    note = "Investimento realizado com sucesso!"
    try:
        for x in portifolio:
            for y in result:
                if x == y["ticker"]:
                    res = y["value"]*float(investment)
                    res_res = int(res*10)
                    result_obj = {
                        "ticker": y["ticker"],
                        "result" : res_res,
                    }
                    result_arr.append(result_obj)
        print(result_arr)
        
        for i in result_arr:
            if i["result"] <= 0:
                note = "Investimento muito baixo"
                color = "alert-warning "
                result_str += i["ticker"]+ " R$ " + str(i["result"]) + " "
            else:
                result_str += i["ticker"]+ " R$ " + str(i["result"]) + " "
    except ValueError:
        return render_template("simple.html", result=0, note="Por favor digite um valor!", color="alert-danger" )
    return render_template("simple.html", result=result_str, note=note, color=color)


if __name__ == "__main__":
    app.run(debug=True)