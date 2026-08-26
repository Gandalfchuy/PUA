#!/usr/bin/env python3
"""
Generador de Documentación en PDF para el Proyecto PUA
Produce:
1. Documentacion_Tecnica_PUA.pdf
2. Guia_Usuario_PUA.pdf
Genera PDFs nativos estándar (PDF 1.4) sin dependencias externas.
"""

import os
import sys
import zlib
import re
from datetime import datetime

class PDFBuilder:
    def __init__(self, title="Documento", subtitle="", doc_type="TÉCNICA"):
        self.title = title
        self.subtitle = subtitle
        self.doc_type = doc_type
        self.pages = []  # List of page content streams (strings)
        self.page_width = 612.0   # Letter standard width
        self.page_height = 792.0  # Letter standard height
        self.margin_left = 48.0
        self.margin_right = 48.0
        self.margin_top = 54.0
        self.margin_bottom = 54.0
        self.content_width = self.page_width - self.margin_left - self.margin_right
        
        # State
        self.current_stream = []
        self.y = self.page_height - self.margin_top
        self.page_number = 0
        self.toc_entries = [] # (title, page)

    def _latin1_escape(self, text):
        if not text:
            return ""
        # Replacements for common unicode characters to WinAnsi / Latin-1
        repl = {
            'á': '\xe1', 'é': '\xe9', 'í': '\xed', 'ó': '\xf3', 'ú': '\xfa',
            'Á': '\xc1', 'É': '\xc9', 'Í': '\xcd', 'Ó': '\xd3', 'Ú': '\xda',
            'ñ': '\xf1', 'Ñ': '\xd1', 'ü': '\xfc', 'Ü': '\xdc',
            '¿': '\xbf', '¡': '\xa1', '—': '-', '–': '-', '“': '"', '”': '"',
            '‘': "'", '’': "'", '•': '*', '→': '->', '✅': '[OK]', '❌': '[X]',
            '🚨': '[ALERTA]', '🔒': '[SEGURIDAD]', '⚡': '[INFO]'
        }
        res = []
        for ch in str(text):
            if ch in repl:
                res.append(repl[ch])
            elif ord(ch) < 256:
                res.append(ch)
            else:
                res.append('?')
        s = "".join(res)
        s = s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        return s

    def new_page(self, is_cover=False):
        if self.current_stream:
            self.pages.append("\n".join(self.current_stream))
            self.current_stream = []
        self.page_number += 1
        self.y = self.page_height - self.margin_top
        
        if not is_cover:
            # Draw header
            self._draw_header()
        return self

    def _draw_header(self):
        # Header text & line
        stream = self.current_stream
        stream.append("q")
        stream.append("0.4 0.45 0.55 rg") # gray text
        stream.append(f"BT /F1 8 Tf {self.margin_left} {self.page_height - 36} Td ({self._latin1_escape(self.title)}) Tj ET")
        stream.append(f"BT /F2 8 Tf {self.page_width - self.margin_right - 60} {self.page_height - 36} Td ({self._latin1_escape(self.doc_type)}) Tj ET")
        # Line
        stream.append("0.8 0.85 0.9 RG 0.75 w")
        stream.append(f"{self.margin_left} {self.page_height - 42} m {self.page_width - self.margin_right} {self.page_height - 42} l S")
        stream.append("Q")

    def _draw_footer(self, total_pages=1):
        # Footers are appended during finalize
        pass

    def check_space(self, needed):
        if self.y - needed < self.margin_bottom:
            self.new_page()

    def draw_cover(self, author="Equipo de Desarrollo PUA", version="1.0.0", date_str="Agosto 2026"):
        self.new_page(is_cover=True)
        s = self.current_stream
        s.append("q")
        
        # Header banner (Deep Navy)
        s.append("0.08 0.18 0.36 rg") # #142E5C
        s.append(f"0 {self.page_height - 240} {self.page_width} 240 re f")
        
        # Decorative accent line (Cyan/Teal)
        s.append("0.01 0.52 0.78 rg") # #0284C7
        s.append(f"0 {self.page_height - 246} {self.page_width} 6 re f")
        
        # Cover Category Badge
        s.append("1 1 1 rg")
        s.append(f"BT /F2 12 Tf {self.margin_left} {self.page_height - 75} Td ({self._latin1_escape('SISTEMA PUA  |  DOCUMENTO OFICIAL')}) Tj ET")
        
        # Main Title
        s.append("1 1 1 rg")
        s.append(f"BT /F2 26 Tf {self.margin_left} {self.page_height - 125} Td ({self._latin1_escape(self.title)}) Tj ET")
        
        # Subtitle
        s.append("0.85 0.92 1.0 rg")
        s.append(f"BT /F1 13 Tf {self.margin_left} {self.page_height - 160} Td ({self._latin1_escape(self.subtitle)}) Tj ET")
        
        # System Tagline
        s.append("0.7 0.8 0.95 rg")
        s.append(f"BT /F3 10 Tf {self.margin_left} {self.page_height - 190} Td ({self._latin1_escape('Plataforma Integral de Registro, Georreferenciacion y Procesos de Reeducacion')}) Tj ET")
        
        # Metadata Card
        card_y = self.page_height - 400
        s.append("0.96 0.97 0.99 rg") # Light background
        s.append(f"{self.margin_left} {card_y} {self.content_width} 110 re f")
        s.append("0.8 0.85 0.9 RG 1 w")
        s.append(f"{self.margin_left} {card_y} {self.content_width} 110 re S")
        
        s.append("0.1 0.2 0.35 rg")
        s.append(f"BT /F2 11 Tf {self.margin_left + 18} {card_y + 85} Td ({self._latin1_escape('INFORMACION DEL DOCUMENTO')}) Tj ET")
        
        s.append("0.25 0.3 0.4 rg")
        s.append(f"BT /F2 9 Tf {self.margin_left + 18} {card_y + 60} Td ({self._latin1_escape('Version:')}) Tj ET")
        s.append(f"BT /F1 9 Tf {self.margin_left + 90} {card_y + 60} Td ({self._latin1_escape(version)}) Tj ET")
        
        s.append(f"BT /F2 9 Tf {self.margin_left + 18} {card_y + 40} Td ({self._latin1_escape('Fecha:')}) Tj ET")
        s.append(f"BT /F1 9 Tf {self.margin_left + 90} {card_y + 40} Td ({self._latin1_escape(date_str)}) Tj ET")
        
        s.append(f"BT /F2 9 Tf {self.margin_left + 18} {card_y + 20} Td ({self._latin1_escape('Elaborado por:')}) Tj ET")
        s.append(f"BT /F1 9 Tf {self.margin_left + 90} {card_y + 20} Td ({self._latin1_escape(author)}) Tj ET")
        
        # Abstract box
        abs_y = card_y - 130
        s.append("0.92 0.95 0.98 rg")
        s.append(f"{self.margin_left} {abs_y} {self.content_width} 95 re f")
        s.append("0.01 0.52 0.78 RG 2 w")
        s.append(f"{self.margin_left} {abs_y} m {self.margin_left} {abs_y + 95} l S") # Left bar
        
        s.append("0.08 0.18 0.36 rg")
        s.append(f"BT /F2 10 Tf {self.margin_left + 15} {abs_y + 75} Td ({self._latin1_escape('RESUMEN Y CONFIDENCIALIDAD')}) Tj ET")
        s.append("0.3 0.35 0.45 rg")
        s.append(f"BT /F1 8.5 Tf {self.margin_left + 15} {abs_y + 55} Td ({self._latin1_escape('Este documento contiene informacion operativa y tecnologica del Sistema PUA.')}) Tj ET")
        s.append(f"BT /F1 8.5 Tf {self.margin_left + 15} {abs_y + 40} Td ({self._latin1_escape('Su distribucion esta reservada para personal tecnico, administrativo y operativo.')}) Tj ET")
        s.append(f"BT /F1 8.5 Tf {self.margin_left + 15} {abs_y + 25} Td ({self._latin1_escape('Prohibida su reproduccion total o parcial sin autorizacion expresa.')}) Tj ET")

        s.append("Q")

    def add_h1(self, text, add_toc=True):
        self.check_space(55)
        if add_toc:
            self.toc_entries.append((text, self.page_number))
        self.y -= 14
        s = self.current_stream
        s.append("q")
        # Banner
        s.append("0.93 0.96 0.99 rg") # soft blue
        s.append(f"{self.margin_left} {self.y - 6} {self.content_width} 24 re f")
        s.append("0.08 0.28 0.55 rg") # navy bar
        s.append(f"{self.margin_left} {self.y - 6} 4 24 re f")
        
        s.append("0.08 0.18 0.36 rg")
        s.append(f"BT /F2 13 Tf {self.margin_left + 12} {self.y} Td ({self._latin1_escape(text)}) Tj ET")
        s.append("Q")
        self.y -= 24

    def add_h2(self, text):
        self.check_space(38)
        self.y -= 10
        s = self.current_stream
        s.append("q")
        s.append("0.01 0.52 0.78 rg")
        s.append(f"BT /F2 11 Tf {self.margin_left} {self.y} Td ({self._latin1_escape(text)}) Tj ET")
        # Underline
        s.append("0.85 0.9 0.95 RG 0.5 w")
        s.append(f"{self.margin_left} {self.y - 3} m {self.margin_left + self.content_width} {self.y - 3} l S")
        s.append("Q")
        self.y -= 16

    def add_h3(self, text):
        self.check_space(26)
        self.y -= 6
        s = self.current_stream
        s.append("q")
        s.append("0.2 0.25 0.35 rg")
        s.append(f"BT /F2 9.5 Tf {self.margin_left} {self.y} Td ({self._latin1_escape(text)}) Tj ET")
        s.append("Q")
        self.y -= 13

    def add_paragraph(self, text, font="F1", size=8.5, color=(0.2, 0.25, 0.3), space_after=6):
        words = str(text).split()
        if not words:
            return
        
        # Average character width approx (Helvetica ~0.52 of font size)
        char_width = size * 0.50
        max_chars_per_line = int(self.content_width / char_width)
        
        lines = []
        current_line = []
        current_len = 0
        
        for w in words:
            if current_len + len(w) + 1 <= max_chars_per_line:
                current_line.append(w)
                current_len += len(w) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [w]
                current_len = len(w)
        if current_line:
            lines.append(" ".join(current_line))
            
        line_height = size * 1.35
        needed = len(lines) * line_height + space_after
        self.check_space(needed)
        
        s = self.current_stream
        s.append("q")
        s.append(f"{color[0]} {color[1]} {color[2]} rg")
        for line in lines:
            s.append(f"BT /{font} {size} Tf {self.margin_left} {self.y} Td ({self._latin1_escape(line)}) Tj ET")
            self.y -= line_height
        s.append("Q")
        self.y -= space_after

    def add_bullet(self, title, text, font="F1", size=8.5):
        char_width = size * 0.50
        bullet_indent = 16
        available_width = self.content_width - bullet_indent
        max_chars = int(available_width / char_width)
        
        full_text = f"{title}: {text}" if title else text
        words = full_text.split()
        
        lines = []
        curr = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 <= max_chars:
                curr.append(w)
                curr_len += len(w) + 1
            else:
                if curr:
                    lines.append(" ".join(curr))
                curr = [w]
                curr_len = len(w)
        if curr:
            lines.append(" ".join(curr))
            
        line_height = size * 1.35
        needed = len(lines) * line_height + 4
        self.check_space(needed)
        
        s = self.current_stream
        s.append("q")
        # Bullet dot
        s.append("0.01 0.52 0.78 rg")
        s.append(f"{self.margin_left + 4} {self.y + 3} 3 3 re f")
        
        s.append("0.2 0.25 0.3 rg")
        first = True
        for line in lines:
            x_pos = self.margin_left + bullet_indent
            s.append(f"BT /{font} {size} Tf {x_pos} {self.y} Td ({self._latin1_escape(line)}) Tj ET")
            self.y -= line_height
        s.append("Q")
        self.y -= 3

    def add_callout(self, title, text, ctype="info"):
        # ctype: info, success, warning
        colors = {
            "info": ((0.93, 0.96, 0.99), (0.01, 0.52, 0.78), "INFO"),
            "success": ((0.92, 0.98, 0.94), (0.1, 0.65, 0.3), "EXITO"),
            "warning": ((0.99, 0.96, 0.91), (0.85, 0.5, 0.05), "IMPORTANTE")
        }
        bg, border, tag = colors.get(ctype, colors["info"])
        
        # Word wrap text
        char_width = 8.0 * 0.50
        max_chars = int((self.content_width - 24) / char_width)
        words = text.split()
        lines = []
        curr = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 <= max_chars:
                curr.append(w)
                curr_len += len(w) + 1
            else:
                if curr:
                    lines.append(" ".join(curr))
                curr = [w]
                curr_len = len(w)
        if curr:
            lines.append(" ".join(curr))
            
        box_height = 20 + len(lines) * 11 + 6
        self.check_space(box_height + 8)
        
        s = self.current_stream
        s.append("q")
        s.append(f"{bg[0]} {bg[1]} {bg[2]} rg")
        s.append(f"{self.margin_left} {self.y - box_height} {self.content_width} {box_height} re f")
        s.append(f"{border[0]} {border[1]} {border[2]} rg")
        s.append(f"{self.margin_left} {self.y - box_height} 3.5 {box_height} re f")
        
        # Title
        s.append(f"{border[0]} {border[1]} {border[2]} rg")
        s.append(f"BT /F2 8.5 Tf {self.margin_left + 12} {self.y - 12} Td ({self._latin1_escape(f'[{tag}] {title}')}) Tj ET")
        
        # Text
        s.append("0.25 0.3 0.38 rg")
        curr_y = self.y - 23
        for line in lines:
            s.append(f"BT /F1 8 Tf {self.margin_left + 12} {curr_y} Td ({self._latin1_escape(line)}) Tj ET")
            curr_y -= 11
        s.append("Q")
        self.y -= (box_height + 8)

    def add_code_box(self, code_lines, title=None):
        line_height = 10
        box_height = (len(code_lines) * line_height) + (16 if title else 10)
        self.check_space(box_height + 8)
        
        s = self.current_stream
        s.append("q")
        s.append("0.12 0.15 0.2 rg") # Dark terminal background
        s.append(f"{self.margin_left} {self.y - box_height} {self.content_width} {box_height} re f")
        s.append("0.3 0.4 0.5 RG 0.5 w")
        s.append(f"{self.margin_left} {self.y - box_height} {self.content_width} {box_height} re S")
        
        curr_y = self.y - 10
        if title:
            s.append("0.01 0.7 0.9 rg")
            s.append(f"BT /F2 7.5 Tf {self.margin_left + 10} {curr_y} Td ({self._latin1_escape(f'# {title}')}) Tj ET")
            curr_y -= 12
            
        s.append("0.85 0.9 0.95 rg")
        for line in code_lines:
            s.append(f"BT /F4 7.5 Tf {self.margin_left + 10} {curr_y} Td ({self._latin1_escape(line)}) Tj ET")
            curr_y -= line_height
            
        s.append("Q")
        self.y -= (box_height + 8)

    def add_table(self, headers, rows, col_widths=None):
        if not col_widths:
            col_widths = [self.content_width / len(headers)] * len(headers)
            
        header_height = 18
        row_height = 16
        
        total_height = header_height + len(rows) * row_height + 10
        self.check_space(min(total_height, 120))
        
        s = self.current_stream
        s.append("q")
        
        # Header background (Navy)
        s.append("0.08 0.18 0.36 rg")
        s.append(f"{self.margin_left} {self.y - header_height} {self.content_width} {header_height} re f")
        
        # Header text
        s.append("1 1 1 rg")
        x_cur = self.margin_left
        for idx, h in enumerate(headers):
            s.append(f"BT /F2 8 Tf {x_cur + 6} {self.y - 12} Td ({self._latin1_escape(h)}) Tj ET")
            x_cur += col_widths[idx]
            
        self.y -= header_height
        
        # Rows
        for r_idx, row in enumerate(rows):
            self.check_space(row_height + 4)
            # Alternating background
            if r_idx % 2 == 0:
                s.append("0.97 0.98 0.99 rg")
            else:
                s.append("0.93 0.95 0.97 rg")
            s.append(f"{self.margin_left} {self.y - row_height} {self.content_width} {row_height} re f")
            
            # Row borders
            s.append("0.85 0.88 0.92 RG 0.5 w")
            s.append(f"{self.margin_left} {self.y - row_height} {self.content_width} {row_height} re S")
            
            # Text
            s.append("0.2 0.25 0.35 rg")
            x_cur = self.margin_left
            for c_idx, cell in enumerate(row):
                if c_idx < len(col_widths):
                    w = col_widths[c_idx]
                    # truncate if too long
                    cell_str = str(cell)
                    max_c = int(w / 4.8)
                    if len(cell_str) > max_c:
                        cell_str = cell_str[:max_c-3] + "..."
                    s.append(f"BT /F1 7.5 Tf {x_cur + 6} {self.y - 11} Td ({self._latin1_escape(cell_str)}) Tj ET")
                    x_cur += w
            self.y -= row_height
            
        s.append("Q")
        self.y -= 8

    def build_pdf(self, output_path):
        # Finalize last page
        if self.current_stream:
            self.pages.append("\n".join(self.current_stream))
            self.current_stream = []
            
        total_pages = len(self.pages)
        
        # Now we compile the PDF binary objects
        # Object 1: Catalog
        # Object 2: Pages tree
        # Object 3..: Font objects
        # Then page objects & content streams
        
        pdf_objs = [] # list of bytes
        
        def new_obj(content):
            pdf_objs.append(content)
            return len(pdf_objs)
            
        # Placeholder for object IDs
        # We will construct properly
        
        # Object 1: Catalog
        cat_id = 1
        pages_id = 2
        f1_id = 3 # Helvetica
        f2_id = 4 # Helvetica-Bold
        f3_id = 5 # Helvetica-Oblique
        f4_id = 6 # Courier
        f5_id = 7 # Courier-Bold
        
        # We need font objects 3..7
        fonts_dict = f"<< /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R /F4 {f4_id} 0 R /F5 {f5_id} 0 R >>"
        
        # Pre-build pages & contents
        page_obj_ids = []
        content_obj_ids = []
        
        next_id = 8
        for i in range(total_pages):
            page_obj_ids.append(next_id)
            next_id += 1
            content_obj_ids.append(next_id)
            next_id += 1
            
        # 1: Catalog
        cat_data = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode('ascii')
        
        # 2: Pages
        kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
        pages_data = f"<< /Type /Pages /Kids [{kids_str}] /Count {total_pages} >>".encode('ascii')
        
        # Fonts
        f1_data = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        f2_data = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        f3_data = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"
        f4_data = b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>"
        f5_data = b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>"
        
        raw_objs = [
            cat_data,
            pages_data,
            f1_data,
            f2_data,
            f3_data,
            f4_data,
            f5_data
        ]
        
        # Build page objects & content streams
        for idx in range(total_pages):
            p_num = idx + 1
            content_str = self.pages[idx]
            
            # Add footer on content stream if not cover
            if p_num > 1:
                footer_stream = (
                    "\nq\n"
                    "0.5 0.55 0.65 rg\n"
                    "0.85 0.9 0.95 RG 0.75 w\n"
                    f"{self.margin_left} 38 m {self.page_width - self.margin_right} 38 l S\n"
                    f"BT /F1 8 Tf {self.margin_left} 26 Td ({self._latin1_escape('Sistema PUA - Confidencial')}) Tj ET\n"
                    f"BT /F2 8 Tf {self.page_width - self.margin_right - 65} 26 Td ({self._latin1_escape(f'Pagina {p_num} de {total_pages}')}) Tj ET\n"
                    "Q\n"
                )
                content_str += footer_stream
                
            content_bytes = content_str.encode('latin1', errors='replace')
            compressed = zlib.compress(content_bytes)
            
            stream_obj = (
                f"<< /Length {len(compressed)} /Filter /FlateDecode >>\nstream\n".encode('ascii')
                + compressed
                + b"\nendstream"
            )
            
            p_id = page_obj_ids[idx]
            c_id = content_obj_ids[idx]
            
            page_obj = f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {self.page_width} {self.page_height}] /Contents {c_id} 0 R /Resources << /Font {fonts_dict} >> >>".encode('ascii')
            
            raw_objs.append(page_obj)
            raw_objs.append(stream_obj)
            
        # Write PDF binary
        out = bytearray()
        out.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        
        xref_offsets = []
        for i, obj_data in enumerate(raw_objs):
            obj_num = i + 1
            xref_offsets.append(len(out))
            out.extend(f"{obj_num} 0 obj\n".encode('ascii'))
            out.extend(obj_data)
            out.extend(b"\nendobj\n")
            
        xref_start = len(out)
        out.extend(f"xref\n0 {len(raw_objs) + 1}\n".encode('ascii'))
        out.extend(b"0000000000 65535 f \n")
        for offset in xref_offsets:
            out.extend(f"{offset:010d} 00000 n \n".encode('ascii'))
            
        out.extend(
            f"trailer\n<< /Size {len(raw_objs) + 1} /Root {cat_id} 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode('ascii')
        )
        
        with open(output_path, "wb") as f:
            f.write(out)
            
        print(f" PDF generado exitosamente: {output_path} ({len(out)} bytes, {total_pages} paginas)")


def generate_technical_docs(output_path):
    pdf = PDFBuilder(
        title="Documentacion Tecnica PUA",
        subtitle="Especificacion de Arquitectura, Modelo de Datos, APIs y Pruebas",
        doc_type="DOCUMENTO TECNICO"
    )
    
    # Portada
    pdf.draw_cover(
        author="Equipo de Desarrollo y Arquitectura PUA",
        version="1.0.0 (Release Estable)",
        date_str=datetime.now().strftime("%B %Y")
    )
    
    # Página 1: Introducción y Arquitectura
    pdf.new_page()
    pdf.add_h1("1. Introduccion y Objetivos del Sistema")
    pdf.add_paragraph(
        "El Sistema PUA (Plataforma Unica de Agresores) es una solucion de software institucional disenada para "
        "la administracion integral, geolocalizacion, perfilamiento multidimensional y seguimiento operativo de procesos "
        "de reeducacion para personas agresoras. El sistema proporciona a las dependencias gubernamentales, coordinadores "
        "y facilitadores una plataforma segura, robusta y centralizada para la toma de decisiones basada en evidencia."
    )
    
    pdf.add_callout(
        "Mision del Software",
        "Estandarizar la recopilacion de datos sociodemograficos y psicologicos, optimizar la medicion de cumplimiento "
        "en procesos reeducativos y proporcionar georreferenciacion precisa mediante extensiones espaciales GIS.",
        "info"
    )
    
    pdf.add_h2("1.1 Pila Tecnologica (Tech Stack)")
    tech_headers = ["Capa", "Tecnologia", "Version", "Proposito Clave"]
    tech_rows = [
        ["Backend REST API", "FastAPI (Python)", "0.136+", "Servidor asincrono, alto rendimiento y autodocumentacion OpenAPI."],
        ["Capa ORM", "SQLAlchemy", "2.0.49", "Mapeo objeto-relacional, mixins de auditoria y consultas optimizadas."],
        ["Extension GIS", "GeoAlchemy2 / PostGIS", "0.20 / 4326", "Soporte nativo para puntos geograficos EPSG:4326."],
        ["Serializacion", "Pydantic v2", "2.13+", "Validacion estricta de esquemas, CURP y decodificacion PostGIS."],
        ["Frontend SPA", "Angular (Standalone)", "21.2.0", "Arquitectura moderna orientada a componentes independientes y lazy loading."],
        ["Base de Datos", "PostgreSQL", "16+ PostGIS", "Persistencia relacional con integridad referencial y auditoria."]
    ]
    pdf.add_table(tech_headers, tech_rows, [90, 110, 74, 230])
    
    pdf.add_h1("2. Arquitectura Global del Sistema")
    pdf.add_paragraph(
        "La aplicacion opera bajo una arquitectura desacoplada Cliente-Servidor (SPA + REST API) con separacion total "
        "de responsabilidades. El frontend se comunica exclusivamente mediante peticiones HTTPS autenticadas mediante tokens JWT."
    )
    
    pdf.add_bullet("Capa de Presentacion (Angular 21)", "Estructura modular basada en componentes Standalone, carga perezosa de rutas (Lazy Loading) y servicios genericos reutilizables.")
    pdf.add_bullet("Capa de Aplicacion (FastAPI)", "Routers modulares, inyeccion de dependencias para sesiones de base de datos y control de acceso basado en roles (RBAC).")
    pdf.add_bullet("Capa de Datos (PostgreSQL/PostGIS)", "Diseno normalizado con soporte para borrado logico (Soft-Delete) y mixins transversales de auditoria.")

    # Página 2: Modelo de Datos
    pdf.new_page()
    pdf.add_h1("3. Modelo de Datos y Esquema de Base de Datos")
    pdf.add_paragraph(
        "El esquema relacional implementa un patron de auditoria universal (AuditMixin) y catalogo maestro (CatalogoMixin). "
        "La entidad principal 'agresor' concentra la informacion general, mientras que las relaciones complejas se resuelven "
        "a traves de tablas pivote intermedias."
    )
    
    pdf.add_h2("3.1 Entidades Principales")
    ent_headers = ["Tabla", "Clave Primaria", "Descripcion Operativa", "Campos Relevantes"]
    ent_rows = [
        ["usuarios", "id (SERIAL)", "Usuarios del sistema", "username, correo, hashed_password, rol_id, is_active"],
        ["roles", "id (SERIAL)", "Roles de acceso (RBAC)", "nombre (SUPER_ADMIN, etc.), descripcion, activo"],
        ["agresor", "folio (SERIAL)", "Expediente de agresores", "curp, nombre, lugar_nacimiento/residencia/trabajo (POINT)"],
        ["procesoreeducacion", "folio (SERIAL)", "Proceso judicial/reeducativo", "agresor_id, fecha_inicio, denunciante, fiscalia"],
        ["grupo", "folio (SERIAL)", "Sedes y grupos de apoyo", "lugar, ubicacion (POINT SRID 4326), created_at"],
        ["sesion", "folio (SERIAL)", "Catalogo de temas", "nombre, objetivo pedagogico, created_at"],
        ["lista", "id (SERIAL)", "Registro de asistencias", "agresor_id, grupo_id, sesion_id, fecha"]
    ]
    pdf.add_table(ent_headers, ent_rows, [85, 80, 140, 199])
    
    pdf.add_h2("3.2 Mixin de Auditoria Transversal (AuditMixin)")
    pdf.add_paragraph(
        "Todas las tablas operativas heredan automaticamente los siguientes campos de trazabilidad para garantizar integridad:"
    )
    pdf.add_bullet("created_at / updated_at", "Timestamps de creacion y modificacion con valor por defecto del servidor.")
    pdf.add_bullet("created_by / updated_by", "Claves foraneas referenciando a la tabla usuarios(id).")
    pdf.add_bullet("deleted_at / deleted_by / is_deleted", "Mecanismo de borrado logico que preserva la historia de datos.")

    # Página 3: Catálogo de APIs REST
    pdf.new_page()
    pdf.add_h1("4. Catalogo de APIs y Endpoints REST")
    pdf.add_paragraph(
        "Todos los endpoints operan bajo formato JSON (excepto /login que requiere x-www-form-urlencoded). "
        "La autenticacion se realiza mediante el encabezado 'Authorization: Bearer <token>'."
    )
    
    api_headers = ["Metodo", "Ruta Endpoint", "Seguridad", "Descripcion"]
    api_rows = [
        ["POST", "/login", "Publico", "Autentica credenciales y emite token JWT con 8h de vigencia."],
        ["GET", "/agresores", "Autenticado", "Obtiene lista de agresores activos con datos relacionales."],
        ["POST", "/agresores", "Autenticado", "Crea un nuevo expediente validando CURP unica y coordenadas."],
        ["GET", "/agresores/{folio}", "Autenticado", "Consulta un expediente individual decodificando PostGIS a JSON."],
        ["PUT", "/agresores/{folio}", "Autenticado", "Actualiza informacion sociodemografica y relaciones M:N."],
        ["DELETE", "/agresores/{folio}", "SUPER_ADMIN", "Ejecuta borrado logico (is_deleted=True, registra deleted_by)."],
        ["GET / POST", "/proceso-reeducacion", "Autenticado", "Administra expedientes de reeducacion asociados a agresores."],
        ["GET / PUT", "/proceso-reeducacion/{folio}", "Autenticado", "Consulta y actualiza detalles de carpetas y fiscalia."],
        ["GET / POST", "/grupos", "Autenticado", "Lista y registra sedes operativas con coordenadas PostGIS."],
        ["GET / POST", "/sesiones", "Autenticado", "Gestiona el catalogo de temas y objetivos pedagogicos."],
        ["GET / POST", "/lista", "Autenticado", "Registra y consulta asistencias de agresores a sesiones."],
        ["CRUD", "/catalogos/{tipo}", "Autenticado/Admin", "15 Catálogos dinamicos creados con patron Factory."]
    ]
    pdf.add_table(api_headers, api_rows, [55, 145, 90, 214])
    
    pdf.add_h2("4.1 Patron Factory en Routers de Catalogos")
    pdf.add_paragraph(
        "Para evitar la duplicacion de codigo en los 15 catalogos del sistema (adicciones, estados civiles, etc.), "
        "se implemento 'crear_router_catalogo()' en backend/app/routers/factory.py, que autogenera endpoints "
        "POST, GET (con filtro is_deleted), GET by ID, PUT y DELETE estandarizados con tipado Pydantic."
    )

    # Página 4: Frontend y Pruebas
    pdf.new_page()
    pdf.add_h1("5. Arquitectura del Frontend (Angular 21)")
    pdf.add_paragraph(
        "El frontend utiliza Standalone Components, Reactive Forms y un patron de herencia generica para maximizar la mantenibilidad:"
    )
    pdf.add_bullet("BaseCrudService<TItem, T>", "Servicio generico que provee metodos HTTP estandarizados (obtenerTodos, obtenerPorId, crear, actualizar, eliminar).")
    pdf.add_bullet("BaseCrudComponent<TItem, T>", "Directiva base abstracta que gestiona estado de carga, paginacion reactiva, busqueda en memoria, modales de confirmacion y control de formularios.")
    pdf.add_bullet("Lazy Loading (app.routes.ts)", "Todas las vistas se cargan bajo demanda con loadComponent: () => import(...) para optimizar el bundle inicial.")
    pdf.add_bullet("AuthInterceptor & AuthGuard", "Inyeccion automatica del JWT en peticiones y proteccion de rutas con verificacion SSR-safe (isPlatformBrowser).")

    pdf.add_h1("6. Cobertura de Pruebas Unitarias y Calidad")
    pdf.add_paragraph(
        "El proyecto cuenta con suites de pruebas automatizadas ejecutables de manera local y en pipelines CI/CD:"
    )
    
    test_headers = ["Capa", "Herramienta", "Archivos de Test", "Pruebas", "Estado"]
    test_rows = [
        ["Backend Core", "Python unittest", "test_security.py", "3 tests", "100% OK (Hash bcrypt, JWT)"],
        ["Backend Schemas", "Python unittest", "test_schemas.py", "9 tests", "100% OK (Validacion CURP, GIS)"],
        ["Backend RBAC", "Python unittest", "test_role_verifier.py", "2 tests", "100% OK (Permisos 403/200)"],
        ["Frontend Services", "Vitest + HttpTesting", "8 service specs", "25 tests", "100% OK (BaseCrud y APIs)"],
        ["Frontend Guards", "Vitest", "auth-guard/interceptor", "4 tests", "100% OK (JWT injection)"],
        ["Frontend Views", "Vitest + TestBed", "12 component specs", "11 tests", "100% OK (Instanciacion y UI)"]
    ]
    pdf.add_table(test_headers, test_rows, [85, 85, 110, 60, 164])
    
    pdf.add_callout(
        "Comandos de Ejecucion de Pruebas",
        "Backend: python3 -m unittest discover -s tests -p 'test_*.py' -v\n"
        "Frontend: npx vitest run",
        "success"
    )

    pdf.build_pdf(output_path)


def generate_user_guide(output_path):
    pdf = PDFBuilder(
        title="Guia de Usuario - Sistema PUA",
        subtitle="Manual de Operacion y Procedimientos para Usuarios del Sistema",
        doc_type="GUIA DE USUARIO"
    )
    
    # Portada
    pdf.draw_cover(
        author="Direccion de Tecnologias de Informacion",
        version="1.0 (Manual Operativo)",
        date_str=datetime.now().strftime("%B %Y")
    )
    
    # Página 1: Inicio de Sesión y Navegación
    pdf.new_page()
    pdf.add_h1("1. Acceso al Sistema e Inicio de Sesion")
    pdf.add_paragraph(
        "Bienvenido a la Plataforma Unica de Agresores (PUA). Para acceder al sistema, abra su navegador web "
        "(Google Chrome, Microsoft Edge o Mozilla Firefox) e ingrese a la direccion oficial de la institucion."
    )
    
    pdf.add_h2("1.1 Procedimiento de Ingreso")
    pdf.add_bullet("Paso 1", "Ingrese su correo electronico institucional en el campo 'Correo Institucional'.")
    pdf.add_bullet("Paso 2", "Escriba su contrasena asignada en el campo 'Contrasena'.")
    pdf.add_bullet("Paso 3", "Haga clic en el boton azul 'Iniciar Sesion'.")
    pdf.add_bullet("Paso 4", "El sistema validara sus credenciales y desplegara un mensaje de 'Acceso Autorizado' redirigiendole automaticamente al modulo de Agresores.")
    
    pdf.add_callout(
        "Recomendacion de Seguridad",
        "Nunca comparta su contrasena. Si sospecha que su cuenta ha sido comprometida, notifique de inmediato "
        "al Administrador del Sistema. Siempre cierre su sesion al terminar su jornada.",
        "warning"
    )
    
    pdf.add_h2("1.2 Barra Lateral y Menu de Navegacion")
    pdf.add_paragraph("En el lateral izquierdo de la pantalla encontrara el menu con los modulos principales:")
    pdf.add_bullet("Agresores", "Modulo central para el alta, busqueda y seguimiento de expedientes.")
    pdf.add_bullet("Catalogos", "Consulta y actualizacion de tablas maestras del sistema.")
    pdf.add_bullet("Grupos", "Administracion de sedes y grupos de apoyo con georreferenciacion.")
    pdf.add_bullet("Sesiones", "Catalogo de temas pedagógicos y objetivos de reeducacion.")
    pdf.add_bullet("Listas de Asistencia", "Control diario y filtrado de asistencia por participante y sede.")
    pdf.add_bullet("Cerrar Sesion", "Boton rojo inferior para finalizar la sesion de manera segura.")

    # Página 2: Gestión de Expedientes de Agresores
    pdf.new_page()
    pdf.add_h1("2. Gestion de Expedientes de Agresores")
    pdf.add_paragraph(
        "El modulo de Agresores permite registrar y consultar el historial sociodemografico completo de cada participante. "
        "El formulario de captura esta organizado en 5 pestanas estructuradas para agilizar el llenado:"
    )
    
    pdf.add_h2("2.1 Captura Paso a Paso por Pestanas")
    pdf.add_bullet("Pestana 1: Datos Generales", "Capture CURP (18 caracteres alfanumericos obligatorios), Nombre, Apellido Paterno, Apellido Materno y Edad (minimo 18 anos).")
    pdf.add_bullet("Pestana 2: Georreferenciacion", "Capture coordenadas de Lugar de Nacimiento, Residencia y Trabajo. Puede presionar 'Pegar desde Google Maps' tras copiar un enlace o ingresar latitud y longitud.")
    pdf.add_bullet("Pestana 3: Entorno Familiar", "Registre numero de hijos, hermanos, parejas previas, tipo de relacion familiar y antecedentes de violencia en la infancia.")
    pdf.add_bullet("Pestana 4: Perfil Socioeconomico", "Seleccione situacion academica, situacion laboral, vivienda, rango salarial, religion y sectores sociales de pertenencia.")
    pdf.add_bullet("Pestana 5: Aspectos Psicosociales", "Marque actividades recreativas, posibles adicciones y generos musicales preferidos.")
    
    pdf.add_callout(
        "Georreferenciacion Automatica desde Google Maps",
        "Copie cualquier enlace o coordenada desde Google Maps (ej. '@18.8329,-99.2312') y peguelo en el campo correspondiente. "
        "El sistema extraera y validara las coordenadas automaticamente.",
        "info"
    )

    # Página 3: Procesos de Reeducación y Asistencias
    pdf.new_page()
    pdf.add_h1("3. Procesos de Reeducacion y Seguimiento Judicial")
    pdf.add_paragraph(
        "Dentro de cada expediente de agresor, el sistema permite registrar y dar seguimiento a uno o mas Procesos de Reeducacion:"
    )
    pdf.add_bullet("Apertura de Proceso", "Haga clic en 'Agregar Proceso' dentro del expediente para abrir la ventana modal de captura.")
    pdf.add_bullet("Campos Judiciales", "Registre la fecha de inicio, fecha estimada de termino, nombre del denunciante y numero de expediente/carpeta de fiscalia.")
    pdf.add_bullet("Tipificacion", "Seleccione el motivo de ingreso, tipo de violencia ejercida (psicologica, fisica, economica, etc.) y modalidad de violencia.")
    pdf.add_bullet("Guardado Seguro", "Al guardar, el proceso se enlazara automaticamente al expediente del agresor y actualizara el historial en pantalla.")

    pdf.add_h1("4. Grupos, Sesiones y Control de Asistencia")
    pdf.add_h2("4.1 Grupos y Sedes")
    pdf.add_paragraph(
        "En el modulo de Grupos se registran las sedes donde se imparten los talleres. Cuenta con un boton 'Obtener Ubicacion GPS' "
        "para capturar automaticamente la posicion geografica del dispositivo."
    )
    
    pdf.add_h2("4.2 Control de Listas de Asistencia")
    pdf.add_paragraph(
        "El modulo de Asistencia permite registrar la presencia de los participantes en cada sesion y generar reportes mediante filtros:"
    )
    pdf.add_bullet("Filtro por CURP/Participante", "Escriba la CURP para ver todo el historial de asistencia de una persona.")
    pdf.add_bullet("Filtro por Tema/Sesion", "Consulte que participantes asistieron a un tema pedagogico especifico.")
    pdf.add_bullet("Filtro por Sede y Fecha", "Supervise la asistencia por dia y centro comunitario.")

    # Página 4: Catálogos y FAQ
    pdf.new_page()
    pdf.add_h1("5. Administracion de Catalogos del Sistema")
    pdf.add_paragraph(
        "El modulo de Catalogos permite a los administradores actualizar las opciones desplegables del sistema sin necesidad "
        "de programacion. Seleccione el catalogo deseado en el selector superior (ej. 'Adicciones', 'Sectores Sociales') para "
        "agregar, editar o desactivar registros."
    )
    
    pdf.add_h1("6. Preguntas Frecuentes y Solucion de Problemas (FAQ)")
    
    faq_data = [
        ["Pregunta / Problema", "Causa Probable", "Solucion Recomendada"],
        ["El sistema indica 'CURP ya registrada'", "El agresor ya tiene expediente previo.", "Utilice el buscador para localizar el folio existente en lugar de crear uno nuevo."],
        ["No puedo eliminar un registro", "Falta de permisos de SUPER_ADMIN.", "Solicite la baja del expediente a un usuario con rol de Administrador."],
        ["Error de conexion con el servidor", "Falla en red o servidor detenido.", "Verifique su conexion a internet o contacte a soporte tecnico para verificar el servicio API."],
        ["El mapa no detecta mi ubicacion", "Permisos de GPS bloqueados en navegador.", "Haga clic en el candado junto a la URL del navegador y permita el acceso a 'Ubicacion'."]
    ]
    pdf.add_table(faq_data[0], faq_data[1:], [140, 150, 214])
    
    pdf.add_callout(
        "Mesa de Ayuda y Soporte Tecnico",
        "Para asistencia tecnica, reporte de incidencias o creacion de nuevos usuarios, comuniquese con el "
        "Area de Soporte de Sistemas en soporte@pua.gob.mx.",
        "success"
    )

    pdf.build_pdf(output_path)


if __name__ == "__main__":
    output_dir = "/Users/daredev/Desktop/PUA"
    doc_tech_path = os.path.join(output_dir, "Documentacion_Tecnica_PUA.pdf")
    doc_user_path = os.path.join(output_dir, "Guia_Usuario_PUA.pdf")
    
    print("Iniciando generacion de PDFs...")
    generate_technical_docs(doc_tech_path)
    generate_user_guide(doc_user_path)
    print(" Generacion de documentacion completada.")
