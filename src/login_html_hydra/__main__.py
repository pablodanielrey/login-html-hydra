from .web.app import webapp

if __name__ == "__main__":
   webapp.run(host='0.0.0.0', port=10005, debug=True)
