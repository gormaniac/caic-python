from dataclasses import dataclass

from . import Observation


HTML = str
"""Any string that is valid HTML."""

class ObsItem:
    """Represents a single item found in a section of an observation report."""

    def __init__(self, label: str, contents: str) -> None:
        self.label = label
        self.contents = contents

    @classmethod
    def from_section_item(cls, section_item: HTML):
        """Create an ObsItem from a single item found in an ObsSection."""
        label, contents = cls.parse_section_item(section_item)
        return cls(label, contents)

    @staticmethod
    def parse_section_item(section_item: HTML):
        """Parse the HTML for an item and return the label + contents."""

        return "", ""

class ImageItem(ObsItem):
    """A special item that handles images."""

class ObsSection:
    """Represents the items found in each section of an observation report."""

    def __init__(self, section_items: str) -> None:
        self.items = []

        for item in section_items:
            self.items.append(ObsItem.from_section_item(item))

    @classmethod
    def section_from_page(cls, obs_page: HTML, section_name: str):
        """Extract the named section from the given observation page HTML."""

class ImagesSection(ObsSection):
    """A special object that handles the Images section better."""

@dataclass
class FieldObservation(Observation):
    """A field observation from the CAIC website."""

    details: ObsSection
    location: ObsSection
    weather: ObsSection
    snowpack: ObsSection
    avalanches: ObsSection
    images: ImagesSection

    @classmethod
    def from_obs_page(cls, obs_page: HTML):
        return cls(
            details=ObsSection.section_from_page(obs_page, "Details"),
            location=ObsSection.section_from_page(obs_page, "Location"),
            weather=ObsSection.section_from_page(obs_page, "Weather"),
            snowpack=ObsSection.section_from_page(obs_page, "Snowpack"),
            avalanches=ObsSection.section_from_page(obs_page, "Avalanches"),
            images=ImagesSection.section_from_page(obs_page, "Images"),
        )
