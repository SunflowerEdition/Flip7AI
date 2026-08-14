# game/render/pygame_renderer.py
from pathlib import Path
import math
import pygame

from game.data.cards import CardId
from game.data.game_state import GameState

ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"

NUMBER_SLOTS = 7
MODIFIER_SLOTS = 7
TOTAL_COLS = NUMBER_SLOTS + 1  # +1 extra column: pending-preview (top) / second chance (bottom)

PROBABILITY_ROWS = len(CardId)
PROBABILITY_PANEL_W = 260
PROBABILITY_ROW_H = 24

# --- Palette -----------------------------------------------------------
BG_TOP = (16, 19, 28)
BG_BOTTOM = (9, 11, 17)
PANEL_BG = (28, 32, 44)
PANEL_BG_CURRENT = (36, 41, 58)
PANEL_BORDER = (52, 57, 72)
PANEL_BORDER_CURRENT = (240, 190, 90)
SLOT_BG = (21, 24, 33)
SLOT_BORDER = (58, 63, 78)
TEXT_PRIMARY = (232, 234, 238)
TEXT_SECONDARY = (140, 145, 158)
ACCENT_GOLD = (240, 190, 90)
SHADOW = (0, 0, 0, 90)

STATUS_STYLE = {
    "busted": {"tint": (210, 70, 70, 40), "border": (210, 70, 70), "label": "BUSTED"},
    "frozen": {"tint": (80, 150, 240, 40), "border": (80, 150, 240), "label": "FROZEN"},
    "stayed": {"tint": (150, 155, 165, 35), "border": (150, 155, 165), "label": "STAYED"},
}


class CardRenderer:
    """Full-redraw pygame renderer. Call render(state) after any state change,
    or render_drawn(state, player_idx, card_id) right after a card is drawn
    but before it's applied, to preview where it's headed.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        num_players: int,
        card_size: tuple[int, int] = (72, 100),
        padding: int = 8,
        assets_dir: Path = ASSETS_DIR,
        logging: bool = False,
        steps: bool = False,
    ):
        self.screen = screen
        self.num_players = num_players
        self.card_size = card_size
        self.padding = padding
        self.assets_dir = assets_dir
        self.logging = logging
        self.steps = steps

        m = self._layout_metrics(num_players, card_size, padding)
        self.margin = m["margin"]
        self.title_h = m["title_h"]
        self.label_gutter = m["label_gutter"]
        self.header_h = m["header_h"]
        self.panel_pad = m["panel_pad"]
        self.row_gap = m["row_gap"]
        self.panel_gap = m["panel_gap"]
        self.rows_h = m["rows_h"]
        self.panel_w = m["panel_w"]
        self.panel_h = m["panel_h"]
        self.columns = m["columns"]
        self.rows = m["rows"]
        self.probability_panel_w = m["probability_panel_w"]
        self.probability_panel_h = m["probability_panel_h"]

        self._image_cache: dict[CardId, pygame.Surface] = {}
        self.font_title = pygame.font.SysFont("segoeui,arial", 28, bold=True)
        self.font_header = pygame.font.SysFont("segoeui,arial", 18, bold=True)
        self.font_small = pygame.font.SysFont("segoeui,arial", 13, bold=True)
        self.font_probability = pygame.font.SysFont("segoeui,arial", 14)
        self.font_probability_header = pygame.font.SysFont("segoeui,arial", 16, bold=True)

    # -- layout ---------------------------------------------------------

    @staticmethod
    def _layout_metrics(num_players: int, card_size: tuple[int, int], padding: int) -> dict:
        cw, ch = card_size

        columns = 2
        rows = math.ceil(num_players / columns)

        margin = 24
        title_h = 50
        label_gutter = 0
        header_h = 34
        panel_pad = 14
        row_gap = padding
        panel_gap = 14

        rows_h = 2 * ch + row_gap

        panel_w = panel_pad * 2 + TOTAL_COLS * cw + (TOTAL_COLS - 1) * padding
        panel_h = header_h + panel_pad + rows_h + panel_pad

        probability_panel_w = 260
        probability_panel_h = rows * panel_h + (rows - 1) * panel_gap

        total_w = margin * 2 + 2 * panel_w + panel_gap * 2 + probability_panel_w
        total_h = margin * 2 + title_h + probability_panel_h

        return dict(
            margin=margin,
            title_h=title_h,
            label_gutter=label_gutter,
            header_h=header_h,
            panel_pad=panel_pad,
            row_gap=row_gap,
            panel_gap=panel_gap,
            rows_h=rows_h,
            panel_w=panel_w,
            panel_h=panel_h,
            probability_panel_w=probability_panel_w,
            probability_panel_h=probability_panel_h,
            columns=columns,
            rows=rows,
            total_w=total_w,
            total_h=total_h,
        )

    @classmethod
    def required_window_size(
        cls,
        num_players: int,
        card_size: tuple[int, int] = (72, 100),
        padding: int = 8,
    ) -> tuple[int, int]:
        m = cls._layout_metrics(num_players, card_size, padding)
        return m["total_w"], m["total_h"]

    # -- drawing helpers --------------------------------------------------

    def _load_image(self, card_id: CardId) -> pygame.Surface:
        if card_id not in self._image_cache:
            path = self.assets_dir / f"{card_id.name}.png"
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.smoothscale(image, self.card_size)
            self._image_cache[card_id] = image
        return self._image_cache[card_id]

    def _draw_background(self) -> None:
        w, h = self.screen.get_size()
        for y in range(h):
            t = y / max(h - 1, 1)
            color = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
            pygame.draw.line(self.screen, color, (0, y), (w, y))

    def _draw_shadow(self, rect: pygame.Rect, radius: int, offset: int = 3) -> None:
        shadow_surf = pygame.Surface((rect.width + offset * 2, rect.height + offset * 2), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surf, SHADOW,
            (offset, offset, rect.width, rect.height),
            border_radius=radius,
        )
        self.screen.blit(shadow_surf, (rect.x - offset, rect.y))

    def _draw_card(self, card_id: CardId, x: int, y: int) -> None:
        cw, ch = self.card_size
        rect = pygame.Rect(x, y, cw, ch)
        self._draw_shadow(rect, radius=6)
        self.screen.blit(self._load_image(card_id), (x, y))
        pygame.draw.rect(self.screen, (0, 0, 0), rect, width=1, border_radius=6)

    def _draw_empty_slot(self, x: int, y: int) -> None:
        cw, ch = self.card_size
        rect = pygame.Rect(x, y, cw, ch)
        pygame.draw.rect(self.screen, SLOT_BG, rect, border_radius=6)
        pygame.draw.rect(self.screen, SLOT_BORDER, rect, width=1, border_radius=6)

    def _draw_slot_row(self, cards: list[CardId], x: int, y: int, slot_count: int) -> None:
        cw = self.card_size[0]
        for i in range(slot_count):
            slot_x = x + i * (cw + self.padding)
            if i < len(cards):
                self._draw_card(cards[i], slot_x, y)
            else:
                self._draw_empty_slot(slot_x, y)

    def _panel_rect(self, player_idx: int) -> pygame.Rect:
        col = player_idx % self.columns
        row = player_idx // self.columns

        x = self.margin + col * (self.panel_w + self.panel_gap)

        y = (self.margin + self.title_h + row * (self.panel_h + self.panel_gap))

        return pygame.Rect(x, y, self.panel_w, self.panel_h)

    def _draw_panel(self, state: GameState, player_idx: int) -> pygame.Rect:
        player = state.players[player_idx]
        is_current = player_idx == state.current_player_idx
        panel = self._panel_rect(player_idx)

        status = "busted" if player.busted else "frozen" if player.frozen else "stayed" if player.stayed else None

        # Shadow + panel background
        self._draw_shadow(panel, radius=12, offset=4)
        bg_color = PANEL_BG_CURRENT if is_current else PANEL_BG
        pygame.draw.rect(self.screen, bg_color, panel, border_radius=12)

        # Status tint over the whole panel
        if status:
            tint = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
            pygame.draw.rect(tint, STATUS_STYLE[status]["tint"], tint.get_rect(), border_radius=12)
            self.screen.blit(tint, panel.topleft)

        # Border (gold if current turn, status color if something happened, else neutral)
        border_color = PANEL_BORDER_CURRENT if is_current else (
            STATUS_STYLE[status]["border"] if status else PANEL_BORDER
        )
        border_width = 3 if is_current else (2 if status else 1)
        pygame.draw.rect(self.screen, border_color, panel, width=border_width, border_radius=12)

        # Header: name, score, status badge
        header_y = panel.y + self.panel_pad
        name = f"Player {player_idx + 1}"
        name_color = ACCENT_GOLD if is_current else TEXT_PRIMARY
        self.screen.blit(self.font_header.render(name, True, name_color), (panel.x + self.panel_pad, header_y))

        score_text = f"Score: {player.score}"
        score_surf = self.font_header.render(score_text, True, TEXT_SECONDARY)
        self.screen.blit(score_surf, (panel.right - self.panel_pad - score_surf.get_width(), header_y))

        if status:
            badge_text = STATUS_STYLE[status]["label"]
            badge_surf = self.font_small.render(badge_text, True, (20, 20, 24))
            badge_rect = badge_surf.get_rect()
            badge_rect.width += 16
            badge_rect.height += 8
            badge_rect.midtop = (panel.centerx, header_y - 1)
            pygame.draw.rect(self.screen, STATUS_STYLE[status]["border"], badge_rect, border_radius=10)
            self.screen.blit(badge_surf, badge_surf.get_rect(center=badge_rect.center))

        # Card rows
        rows_x = panel.x + self.panel_pad
        rows_y = panel.y + self.panel_pad + self.header_h
        ch = self.card_size[1]
        self._draw_slot_row(player.number_cards, rows_x, rows_y, NUMBER_SLOTS)

        modifier_y = rows_y + ch + self.row_gap
        self._draw_slot_row(player.modifier_cards, rows_x, modifier_y, MODIFIER_SLOTS)

        # Second chance lives in the extra column, modifier row
        extra_x = rows_x + NUMBER_SLOTS * (self.card_size[0] + self.padding)
        if player.second_chance:
            self._draw_card(CardId.SECOND_CHANCE, extra_x, modifier_y)
        else:
            self._draw_empty_slot(extra_x, modifier_y)

        return panel

    def _draw_title(self, state: GameState) -> None:
        title = self.font_title.render(f"FLIP 7  —  Round {state.round_number}", True, TEXT_PRIMARY)
        self.screen.blit(title, (self.margin, self.margin))

    def _draw_board(self, state: GameState) -> None:
        self._draw_background()
        self._draw_title(state)
        for player_idx in range(self.num_players):
            self._draw_panel(state, player_idx)
        probability_x = self.margin + 2 * self.panel_w + self.panel_gap * 2
        probability_y = self.margin + self.title_h
        self._draw_card_probabilities(state, probability_x, probability_y)

    def _draw_card_probabilities(self, state: GameState, x: int, y: int) -> pygame.Rect:
        panel = pygame.Rect(x, y, self.probability_panel_w, self.probability_panel_h)

        self._draw_shadow(panel, radius=12, offset=4)
        pygame.draw.rect(self.screen, PANEL_BG, panel, border_radius=12)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel, width=1, border_radius=12)

        header_y = panel.y + self.panel_pad

        title = self.font_probability_header.render("Card Probabilities", True, TEXT_PRIMARY)
        self.screen.blit(title, (panel.x + self.panel_pad, header_y))

        total_remaining = int(state.unseen_cards.sum())
        total_text = f"{total_remaining} unseen"
        total_surf = self.font_probability.render(total_text, True, TEXT_SECONDARY)
        self.screen.blit(total_surf, (panel.right - self.panel_pad - total_surf.get_width(), header_y + 2))

        # Column headers
        row_y = header_y + 32

        name_x = panel.x + self.panel_pad
        count_x = panel.right - 75
        probability_x = panel.right - self.panel_pad

        header = self.font_probability.render("Card", True, TEXT_SECONDARY)
        self.screen.blit(header, (name_x, row_y))

        count_header = self.font_probability.render("Left", True, TEXT_SECONDARY)
        self.screen.blit(count_header, (count_x - count_header.get_width(), row_y))

        prob_header = self.font_probability.render("%", True, TEXT_SECONDARY)
        self.screen.blit(prob_header, (probability_x - prob_header.get_width(), row_y))

        row_y += PROBABILITY_ROW_H

        for card_id in CardId:
            remaining = int(state.unseen_cards[card_id])
            probability = remaining / total_remaining if total_remaining > 0 else 0.0

            name = card_id.name.replace("_", " ").title()
            text_color = TEXT_PRIMARY if remaining > 0 else TEXT_SECONDARY

            name_surf = self.font_probability.render(name, True, text_color)
            self.screen.blit(name_surf, (name_x, row_y))

            count_surf = self.font_probability.render(str(remaining), True, text_color)
            count_rect = count_surf.get_rect(right=count_x, top=row_y)
            self.screen.blit(count_surf, count_rect)

            probability_surf = self.font_probability.render(f"{probability * 100:.1f}%", True,
                                                            ACCENT_GOLD if remaining > 0 else TEXT_SECONDARY)
            probability_rect = probability_surf.get_rect(right=probability_x, top=row_y)
            self.screen.blit(probability_surf, probability_rect)

            row_y += PROBABILITY_ROW_H

        return panel

    def _render(self, state: GameState) -> None:
        """Redraws the board to reflect the current, already-applied state."""
        self._draw_board(state)
        pygame.display.flip()
        pygame.time.delay(300)
        self._pump_events()

    def _render_drawn(self, state: GameState, player_idx: int, card_id: CardId) -> None:
        """Draws the board as it currently stands (card NOT yet applied), plus
        a preview of the just-drawn card hovering in the extra column of the
        number row, with a gold glow around that player's panel.
        """
        self._draw_board(state)

        panel = self._panel_rect(player_idx)
        rows_x = panel.x + self.panel_pad
        rows_y = panel.y + self.panel_pad + self.header_h
        extra_x = rows_x + NUMBER_SLOTS * (self.card_size[0] + self.padding)

        # Soft gold glow behind the pending card
        cw, ch = self.card_size
        glow = pygame.Surface((cw + 16, ch + 16), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*ACCENT_GOLD, 70), glow.get_rect(), border_radius=12)
        self.screen.blit(glow, (extra_x - 8, rows_y - 8))

        self._draw_card(card_id, extra_x, rows_y)

        tag = self.font_small.render("DRAWN", True, (20, 20, 24))
        tag_rect = tag.get_rect()
        tag_rect.width += 14
        tag_rect.height += 6
        tag_rect.midbottom = (extra_x + cw // 2, rows_y - 8)
        pygame.draw.rect(self.screen, ACCENT_GOLD, tag_rect, border_radius=8)
        self.screen.blit(tag, tag.get_rect(center=tag_rect.center))

        pygame.draw.rect(self.screen, ACCENT_GOLD, panel, width=3, border_radius=12)

        pygame.display.flip()
        pygame.time.delay(300)
        self._pump_events()

    # -- public API -------------------------------------------------------

    def render(
            self,
            state: GameState,
            drawn_card: bool = False,
            player_idx: int | None = None,
            card_id: CardId | None = None,
            message: str | None = None
    ):
        if self.logging and message is not None:
            print(message)
        if drawn_card:
            if player_idx is None or card_id is None:
                print("ERROR: MISSING PARAMETERS")
                return
            self._render_drawn(state, player_idx, card_id)
        else:
            self._render(state)
        if self.steps:
            input("Press any key to continue...")

    @staticmethod
    def _pump_events() -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit