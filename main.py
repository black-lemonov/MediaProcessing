from director import Director, ThemedTkBuilder, TkBuilder

director = Director()
director.min_app(ThemedTkBuilder(theme='ubuntu')).run()