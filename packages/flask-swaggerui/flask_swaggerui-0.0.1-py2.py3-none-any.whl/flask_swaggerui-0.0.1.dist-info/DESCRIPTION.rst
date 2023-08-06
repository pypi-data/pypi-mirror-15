Copyright (c) 2016 Aaron Halfaker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: This library provides python Flask utilities and static assets for rendering Swagger UI.
        
        # Example
        
        ```python
        from flask import Flask, jsonify
        
        from flask_swaggerui import render_swaggerui, build_static_blueprint
        
        app = Flask(__name__)
        
        
        @app.route('/')
        def root():
            return render_swaggerui(swagger_spec_path="/spec")
        
        
        @app.route('/spec')
        def spec():
            return jsonify({"some swagger": "spec stuff"})
        
        
        # Adds static assets for swagger-ui to path
        app.register_blueprint(build_static_blueprint("swaggerui", __name__))
        
        if __name__ == "__main__":
            app.run(port=8080, debug=True)
        ```
        
Platform: UNKNOWN
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Environment :: Other Environment
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Topic :: Software Development :: Libraries :: Python Modules
