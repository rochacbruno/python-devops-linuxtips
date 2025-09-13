---
title: Template Presenterm
sub_title: Exemplo de apresentação
author: Bruno Rocha - LINUXtips
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

Title Slide
===

<!-- alignment: center -->

Main topic

<!-- pause --> 

Continuation


## Subtitle


Sub topic 


Another Slide
===

- lists
- don't need pause
- presenterm pauses automatically

Another slide
===

Executable code

```bash +exec
echo "Hello, World!"
```

With incremental highlighting

```python +exec {1-2|3-4}
print("Hello, World!")
print("This is a test.")
print("This line is hidden.")
print("This line is also hidden.")
```

Diagram
===

```mermaid +render
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

Layout
===

<!-- column_layout: [1, 2] -->
<!-- column: 0 -->

```python
def hello():
    print("Hello, World!")
```

<!-- column: 1 -->

```python
def goodbye():
    print("Goodbye, World!")
```

Font Size
===

<!-- font_size: 2 -->

Hello, World Big.


Conclusion
===

"Inspirational quote." -- Author



