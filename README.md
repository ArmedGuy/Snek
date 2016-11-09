# Snek - a hacky ORM library for Python 3
![Bla](https://i.imgur.com/hlJGRT0.jpg)

Built by me and @kitzin

### Features
 - Supports different languages through use of "processors" that translate common operations into selected SQL flavor.
 - Create all/drop all approach to tables. Screw migrations. (Our course preaches "DO IT RIGHT FIRST" approach, so we'll abide)
 - Basic CRUD for Models, some extended support for Select's
 - Relations might come - foreign key is foreign concept
 - Ugly use of Python 3 builtins module to pass DB connection from main class to models.


### Opinions (follow or it wont work)
To use Snek Models you need to follow a certain naming scheme to ensure proper function.

Model names should be PascalCase in singular.
For example a table holding data for Tags should have a model named `Tag`.
Defining a foreign key for the table `Tweet` in table `Tag` would have the name `tweet_key`.
Snek will then create an attribute `tweet` in instances of `Tag`, and the attribute `tags` in the `Tweet` model.

Example:
```python
def Tweet(Model):
	...

def Tag(Model):
    ...
	tweet_key = Col.ForeignKey(Tweet)

Tweet.register()
Tag.register()
```
