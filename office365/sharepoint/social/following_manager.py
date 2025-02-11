from office365.sharepoint.base_entity import BaseEntity


class SocialFollowingManager(BaseEntity):
    """Provides methods for managing a user's list of followed actors (users, documents, sites, and tags)."""

    @property
    def entity_type_name(self):
        return "SP.Social.SocialFollowingManager"
