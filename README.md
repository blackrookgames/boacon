<a id="boacon"></a>

# boacon

<a id="boacon.init"></a>

#### init

```python
def init()
```

<a id="boacon.final"></a>

#### final

```python
def final()
```

<a id="boacon.state"></a>

#### state

```python
def state()
```

State of the boacon system

<a id="boacon.panes"></a>

#### panes

```python
def panes()
```

Panes that are being displayed

:raise BCError:
    boacon system is not currently running

<a id="boacon.on_init"></a>

#### on\_init

```python
def on_init()
```

Emitted after the boacon system is initialized

<a id="boacon.on_final"></a>

#### on\_final

```python
def on_final()
```

Emitted before the boacon system is finalized

<a id="boacon.postdraw"></a>

#### postdraw

```python
def postdraw()
```

Emitted after drawing the panes and right before the screen is refreshed

:raise BCError:
    boacon system is not currently running

<a id="boacon.refresh"></a>

#### refresh

```python
def refresh()
```

Refreshes the screen

:raise BCError:
    boacon system is not currently running

<a id="boacon.getch"></a>

#### getch

```python
def getch()
```

Gets a character code from the keyboard

:return:
    Character code (or -1 if no character is pressed)
:raise BCError:
    boacon system is not currently running

<a id="boacon.get_border"></a>

#### get\_border

```python
def get_border()
```

Gets whether or not pane borders are enabled

:raise BCError:
    boacon system is not currently running

<a id="boacon.set_border"></a>

#### set\_border

```python
def set_border(value: bool)
```

Sets whether or not pane borders are enabled

:raise BCError:
    boacon system is not currently running

