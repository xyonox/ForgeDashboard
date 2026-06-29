from nicegui import ui

def header():
    ui.query("body").classes("bg-zinc-950 text-white")
    with ui.header().classes("bg-slate-900 p-5"):
        with ui.row().classes("justify-between w-full"):
            button("Forge", on_click=lambda: ui.navigate.to("/"))
            ui.label("Letz Track").classes("text-lg")
            button("profile", on_click=lambda: ui.navigate.to("/profile"))

def button(name, on_click=None):
    btn = ui.button(name, on_click=on_click)
    btn.classes('bg-[#013220] text-white border border-emerald-500 px-4 py-1 rounded shadow-md hover:bg-emerald-900')
    btn.props("color=none")
    return btn

def card(content=None):
    c = (ui.card()
            .classes("bg-[#013220] text-white border border-emerald-500 px-4 py-1 rounded shadow-md"))

    return c

def select(
    options,
    label="",
    value=None,
    with_input=False,
    on_change=None,
):
    s = ui.select(
        options=options,
        label=label,
        value=value,
        with_input=with_input,
        on_change=on_change,
    )

    s.classes("w-64 text-white")
    s.props(
        'popup-content-class="text-white bg-[#013220]" '
        'input-class="text-white"'
    )

    return s