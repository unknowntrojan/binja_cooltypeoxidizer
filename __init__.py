from mailbox import linesep
from typing import List
from binaryninja import (
    LinearViewObject,
    RenderLayer,
    DisassemblyTextLine,
    InstructionTextTokenType,
    RenderLayerDefaultEnableState,
    LinearDisassemblyLine,
    logger,
)

# Only numeric types
rust = {
    "uint8_t": "u8",
    "uint16_t": "u16",
    "uint32_t": "u32",
    "uint64_t": "u64",
    "uint128_t": "u128",
    "int8_t": "i8",
    "int16_t": "i16",
    "int32_t": "i32",
    "int64_t": "i64",
    "int128_t": "i128",
    "float": "f32",
    "double": "f64",
    "size_t": "usize",
    "ssize_t": "isize",
}


def process_line_graph(line: DisassemblyTextLine) -> DisassemblyTextLine:
    for token in line.tokens:
        if token.type is InstructionTextTokenType.KeywordToken:
            if token.text in rust:
                token.text = rust[token.text]
                token.width = len(token.text)

    return line


def process_line_linear(line: LinearDisassemblyLine) -> LinearDisassemblyLine:
    for token in line.contents.tokens:
        if token.type is InstructionTextTokenType.KeywordToken:
            if token.text in rust:
                token.text = rust[token.text]
                token.width = len(token.text)

    return line


class OxidizerLayer(RenderLayer):
    name = "Oxidize Types"
    default_enable_state = (
        RenderLayerDefaultEnableState.DisabledByDefaultRenderLayerDefaultEnableState
    )

    def __init__(self):
        self.handle = None
        super().__init__()

    def apply_to_high_level_il_block(self, block, lines):
        return super().apply_to_high_level_il_block(
            block, [process_line_graph(line) for line in lines]
        )

    def apply_to_high_level_il_body(
        self, function, lines: List[LinearDisassemblyLine]
    ) -> List[LinearDisassemblyLine]:
        return super().apply_to_high_level_il_body(
            function, [process_line_linear(line) for line in lines]
        )

    def apply_to_misc_linear_lines(
        self, obj: LinearViewObject, prev, next, lines: List[LinearDisassemblyLine]
    ) -> List[DisassemblyTextLine]:
        if len(lines) > 10:
            return super().apply_to_misc_linear_lines(obj, prev, next, lines)

        return super().apply_to_misc_linear_lines(
            obj, prev, next, [process_line_linear(line) for line in lines]
        )

    def apply_to_linear_view_object(
        self,
        obj: LinearViewObject,
        prev: LinearViewObject | None,
        next: LinearViewObject | None,
        lines: List[LinearDisassemblyLine],
    ) -> List[LinearDisassemblyLine]:
        return super().apply_to_linear_view_object(
            obj, prev, next, [process_line_linear(line) for line in lines]
        )


OxidizerLayer.register()
