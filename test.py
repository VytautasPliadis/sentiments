title_lt = self.clean_titles(element.get_text().strip())
text_bytes = title_lt.encode('latin-1')
title_lt = text_bytes.decode('utf-8', errors='ignore')
self.title_list_lt.append(title_lt)