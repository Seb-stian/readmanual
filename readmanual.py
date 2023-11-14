from os.path import basename
from sys import argv
from glob import glob
from html import escape
from marko import parse
from marko.element import Element
from marko.inline import InlineElement, RawText, Emphasis, StrongEmphasis, Link, Image, CodeSpan, LineBreak
from marko.block import Document, Heading, BlockElement, BlankLine, Paragraph, List, ListItem, Quote, ThematicBreak, FencedCode

class HtmlConstants:
    START_TO_LANGUAGE_CODE = """<!DOCTYPE html>
<html lang=\""""
    LANGUAGE_CODE_TO_TITLE = """\">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""
    TITLE_TO_SECTIONS_LISTING = """</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    <!-- <link rel="stylesheet" href="https://unpkg.com/@highlightjs/cdn-assets@11.9.0/styles/default.min.css"> -->
    <style>
        .hljs {
            display: block;
            overflow-x: auto;
            padding: 0.5em;
            background: #282a36;
        }

        .hljs-built_in,
        .hljs-selector-tag,
        .hljs-section,
        .hljs-link {
            color: #8be9fd;
        }

        .hljs-keyword {
            color: #ff79c6;
        }

        .hljs,
        .hljs-subst {
            color: #f8f8f2;
        }

        .hljs-title,
        .hljs-attr,
        .hljs-meta-keyword {
        font-style: italic;
            color: #50fa7b;
        }

        .hljs-string,
        .hljs-meta,
        .hljs-name,
        .hljs-type,
        .hljs-symbol,
        .hljs-bullet,
        .hljs-addition,
        .hljs-variable,
        .hljs-template-tag,
        .hljs-template-variable {
            color: #f1fa8c;
        }

        .hljs-comment,
        .hljs-quote,
        .hljs-deletion {
            color: #6272a4;
        }

        .hljs-keyword,
        .hljs-selector-tag,
        .hljs-literal,
        .hljs-title,
        .hljs-section,
        .hljs-doctag,
        .hljs-type,
        .hljs-name,
        .hljs-strong {
            font-weight: bold;
        }

        .hljs-literal,
        .hljs-number {
            color: #bd93f9;
        }

        .hljs-emphasis {
            font-style: italic;
        }
    </style>
    <style>
        :root {
            --text-color: white;
            --select-color: cyan;
            --background-main: black;
            --background-secondary: #333;
            --navigation-height: 70px;
            --navigation-border: 2px;
            --sidebar-width: 250px;
            --content-vertical-padding: 10px;
        }

        body {
            margin: 0;
            color: var(--text-color);
            background-color: var(--background-main);
            font-family: 'Roboto', sans-serif;
        }

        #navigation {
            position: sticky;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0px 10px 0px 10px;
            top: 0;
            height: var(--navigation-height);
            background-color: var(--background-main);
            border-bottom: var(--navigation-border) solid var(--text-color);
        }

        #navigation > button {
            border: medium solid var(--text-color);
            border-radius: 15px;
            color: var(--text-color);
            background: none;
            padding: 10px;
            cursor: pointer;
        }

        #navigation > button:hover {
            color: var(--select-color);
        }

        #navigation > button:active {
            background-color: var(--select-color);
            color: var(--text-color);
        }

        #sidebar {
            position: fixed;
            top: calc(var(--navigation-height) + var(--navigation-border));
            left: 0;
            height: calc(100vh - var(--navigation-height) - var(--navigation-border));
            width: var(--sidebar-width);
            background-color: var(--background-secondary);
            overflow-y: auto;
        }

        #sidebar ul {
            list-style-type: none;
            padding-inline-start: 20px;
        }

        a {
            color: var(--select-color);
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        #content {
            margin-left: var(--sidebar-width);
            padding: var(--content-vertical-padding) 40px var(--content-vertical-padding) 40px;
            height: calc(100vh - var(--navigation-height) - var(--navigation-border) - var(--content-vertical-padding) * 2);
            overflow-y: scroll;
        }

        h1, h2, h3, h4, h5, h6, p {
            margin-top: 0;
            margin-bottom: 10px;
        }

        p {
            margin-bottom: 7px;
        }

        blockquote {
            background-color: var(--background-secondary);
            padding-block-start: 1em;
            margin-block-start: 0;
            padding-block-end: 1em;
            margin-block-end: 0;
            padding-inline-start: 40px;
            margin-inline-start: 0;
            padding-inline-end: 40px;
            margin-inline-end: 0;
            border-left: 5px solid var(--text-color);
        }

        blockquote > p:last-child {
            margin-bottom: 0;
        }

        code {
            font-size: large;
        }
    </style>
    <script src="https://unpkg.com/@highlightjs/cdn-assets@11.9.0/highlight.min.js"></script>
    <script>
        window.onload = () => {
            hljs.highlightAll();
            const sections = ["""
    SECTIONS_LISTING_TO_CUSTOM_CSS = """];
            function showSection(selected) {
                for (const section of sections) {
                    for (const e of document.getElementsByClassName(section)) {
                        console.log(e.tagName);
                        if (e.tagName === "BUTTON") continue;
                        e.style.display = section === selected ? "block" : "none";
                    }
                }
            }
            showSection(sections[0]);
            for (const section of sections) {
                for (const e of document.getElementsByClassName(section)) {
                    if (e.tagName !== "BUTTON") continue;
                    e.addEventListener("click", () => {
                        showSection(section);
                    });
                }
            }
        };
    </script>"""
    CUSTOM_CSS_TO_NAVIGATION = """
</head>
<body>
    <nav id="navigation">"""
    NAVIGATION_TO_SIDEBAR = """
    </nav>
    <aside id="sidebar">
        <nav>
"""
    SIDEBAR_TO_CONTENT = """        </nav>
    </aside>

    <div id="content">
"""
    CONTENT_TO_CUSTOM_JS = """
        <div style="height: 50px;"></div>
    </div>
"""
    CUSTOM_JS_TO_END = """</body>
</html>"""

class Uniquifier:
    def __init__(self) -> None:
        self.__memory = set()

    def uniquify(self, value: str) -> str:
        value = ''.join([c for c in value.lower().replace('_', ' ').replace('-', ' ') if c.isalpha() or c == ' '])
        value = '-'.join(value.split())
        if value not in self.__memory:
            self.__memory.add(value)
            return value
        
        index = 1
        while f'{value}-{index}' in self.__memory:
            index += 1
        return f'{value}-{index}'

class ReadmanualOptions:
    def __init__(self, files: list[str], name: str, languageCode: str, outputFile: str) -> None:
        self.files = files
        self.name = name
        self.languageCode = languageCode
        self.outputFile = outputFile

    @staticmethod
    def from_args(args: list[str]) -> 'ReadmanualOptions':
        files = []
        name = 'Manual'
        language = 'en'
        output = 'manual.html'
        while True:
            if not args:
                break
            arg = args.pop(0)

            if arg.startswith('-'):
                if arg == '-l' or arg == '--language':
                    language = args.pop(0)
                elif arg == '-o' or arg == '--output':
                    output = args.pop(0)
                elif arg == '-n' or arg == '--name':
                    name = args.pop(0)
                else:
                    raise Exception(f'Unknown flag "{arg}"')
                continue
            
            files += glob(arg)
        return ReadmanualOptions(files, name, language, output)

class ReadmanualGenerator:
    def __init__(self, options: ReadmanualOptions) -> None:
        self.__options = options

    @staticmethod
    def __get_text(element: Element) -> str:
        buffer = []
        if isinstance(element, BlockElement):
            for child in element.children:
                buffer.append(ReadmanualGenerator.__get_text(child))
        elif isinstance(element, InlineElement):
            if isinstance(element.children, str):
                buffer.append(element.children)
            else:
                for child in element.children:
                    buffer.append(ReadmanualGenerator.__get_text(child))
        else:
            raise Exception(f'Unsupported element type {element.get_type()}')
        return ''.join(buffer)
    
    @staticmethod
    def __get_hmtl(element: Element, indent: str = '            ', attribute: str = '') -> str:
        buffer = []
        write = lambda x: buffer.append(x)
        writeln = lambda x: buffer.append(x + '\r\n')
        writechildren = lambda: [write(ReadmanualGenerator.__get_hmtl(child, '')) for child in element.children]
        writerecursive = lambda: (write(element.children) if isinstance(element.children, str) else writechildren()) if hasattr(element, 'children') else None

        if isinstance(element, BlankLine):
            writeln(f'{indent}<br>')
        elif isinstance(element, Heading):
            write(f'{indent}<h{element.level}{" " + attribute if attribute else ""}>')
            writechildren()
            writeln(f'</h{element.level}>')
        elif isinstance(element, Paragraph):
            write(f'{indent}<p>')
            writechildren()
            writeln('</p>')
        elif isinstance(element, Emphasis):
            write(f'{indent}<i>')
            writerecursive()
            write('</i>')
        elif isinstance(element, StrongEmphasis):
            write(f'{indent}<strong>')
            writerecursive()
            write('</strong>')
        elif isinstance(element, RawText):
            write(element.children)
        elif isinstance(element, List):
            writeln('<ol>' if element.ordered else '<ul>')
            writechildren()
            writeln('</ol>' if element.ordered else '</ul>')
        elif isinstance(element, ListItem):
            write('<li>')
            writechildren()
            write('</li>')
        elif isinstance(element, Link):
            write(f'<a href="{element.dest}">')
            writerecursive()
            write('</a>')
        elif isinstance(element, Image):
            alt = ReadmanualGenerator.__get_text(element)
            write(f'<img src="{element.dest}" alt="{alt}">')
        elif isinstance(element, Quote):
            writeln('<blockquote>')
            writechildren()
            writeln('</blockquote>')
        elif isinstance(element, CodeSpan):
            write('<code>')
            writerecursive()
            write('</code>')
        elif isinstance(element, ThematicBreak):
            writeln('<hr>')
        elif isinstance(element, LineBreak):
            write('<br>')
        elif isinstance(element, FencedCode):
            attribute = f' class="language-{element.lang}"' if element.lang else ''
            write(f'<pre><code{attribute}>')
            write('\r\n'.join([raw.children for raw in element.children]))
            writeln(f'</code></pre>')
        else:
            raise Exception(f'Unsupported element type {element.get_type()}')
        return ''.join(buffer)

    @staticmethod
    def __document_to_html(section: str, document: Document, navigation_buffer: list[str], body_buffer: list[str], names: Uniquifier) -> None:
        bwrite = lambda x: body_buffer.append(x)
        bwriteln = lambda x: body_buffer.append(x + '\r\n')
        nwriteln = lambda x: navigation_buffer.append(x + '\r\n')

        heading_level = 1

        nwriteln(f'             <ul class="{section}">')
        bwriteln(f'        <div class="{section}">')

        for child in document.children:
            attribute = ''
            if isinstance(child, Heading):
                heading = ReadmanualGenerator.__get_text(child)
                heading_id = names.uniquify(heading)
                attribute = f'id="{heading_id}"'
                while heading_level != child.level:
                    nwriteln('             ' + ('<ul>' if heading_level < child.level else '</ul>'))
                    heading_level += 1 if child.level > heading_level else -1
                nwriteln(f'             <li><a href="#{heading_id}">{heading}</a></li>')
            bwrite(ReadmanualGenerator.__get_hmtl(child, attribute=attribute))

        while heading_level > 1:
            nwriteln('             </ul>')
            heading_level -= 1

        bwriteln('        </div>')
        nwriteln(f'             </ul>')

    def generate(self) -> None:
        if not self.__options.files:
            raise Exception('No input files')

        md_files, css_files, js_files = [], [], []
        for file in self.__options.files:
            if file.endswith('.md'):
                md_files.append(file)
            elif file.endswith('.css'):
                css_files.append(file)
            elif file.endswith('.js'):
                js_files.append(file)
            else:
                raise Exception(f'Unsupported input file extension (file {file})')
        
        uniques = Uniquifier()
        md_sections = [uniques.uniquify(f'section-{basename(file)}') for file in md_files]

        md_documents: list[Document] = []
        md_titles: list[str] = []
        for file in md_files:
            with open(file, encoding='utf-8') as md:
                doc = parse(md.read())
                md_documents.append(doc)

                # Use level 1 heading or filename
                if len(doc.children) > 0 and isinstance(doc.children[0], Heading) and doc.children[0].level == 1:
                    md_titles.append(ReadmanualGenerator.__get_text(doc.children[0]))
                else:
                    md_titles.append(basename(file))
 
        buffer = [
            HtmlConstants.START_TO_LANGUAGE_CODE,
            self.__options.languageCode,
            HtmlConstants.LANGUAGE_CODE_TO_TITLE,
            escape(self.__options.name),
            HtmlConstants.TITLE_TO_SECTIONS_LISTING,
            ', '.join(f'"{section}"' for section in md_sections),
            HtmlConstants.SECTIONS_LISTING_TO_CUSTOM_CSS,
        ]

        for file in css_files:
            buffer.append('<style>')
            with open(file, encoding='utf-8') as css:
                buffer.append(css.read())
            buffer.append('</style>')

        buffer.append(HtmlConstants.CUSTOM_CSS_TO_NAVIGATION)

        for section, title in zip(md_sections, md_titles):
            buffer.append(f"""
        <button type="button" class="{section}">{escape(title)}</button>""")
        
        buffer.append(HtmlConstants.NAVIGATION_TO_SIDEBAR)

        content_buffer: list[str] = []
        for section, document in zip(md_sections, md_documents):
            ReadmanualGenerator.__document_to_html(section, document, buffer, content_buffer, uniques)

        buffer.append(HtmlConstants.SIDEBAR_TO_CONTENT)
        buffer += content_buffer

        buffer.append(HtmlConstants.CONTENT_TO_CUSTOM_JS)

        for file in js_files:
            buffer.append('<script>')
            with open(file, encoding='utf-8') as js:
                buffer.append(js.read())
            buffer.append('</script>')

        buffer.append(HtmlConstants.CUSTOM_JS_TO_END)

        with open(self.__options.outputFile, 'wb') as output:
            for text in buffer:
                output.write(text.encode())

if __name__ == "__main__":
    args: list[str] = argv[1:]

    # If no files are set, use all Markdown, CSS and JS files in directory
    if len([arg for arg in args if not arg.startswith('-')]) == 0:
        args = ['*.md', '*.css', '*.js'] + args
    
    options = ReadmanualOptions.from_args(args)
    ReadmanualGenerator(options).generate()
