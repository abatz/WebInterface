def dynamic_png():
    try:
        plt.title("Dynamic PNG")
        for i in range(5): plt.plot(sorted(numpy.random.randn(25)))
        rv = StringIO.StringIO()
        plt.savefig(rv, format="png")
        plt.clf()
        return """<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip()
    finally:
        plt.clf()


def dynamic_svg():
    try:
        plt.title("Dynamic SVG")
        for i in range(5): plt.plot(sorted(numpy.random.randn(25)))
        rv = StringIO.StringIO()
        plt.savefig(rv, format="svg")
        return rv.getvalue().partition("-->")[-1]
    finally:
        plt.clf()

try: dynamic_png()  # crashes first time because it can't cache fonts
except: logging.exception("don't about it")
