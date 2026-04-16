from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import SpeakerAgentOutput, VenueAgentOutput
from eventforge.utils.logging import get_logger

logger = get_logger(__name__)


class EventOpsAgent(BaseAgent):
    """
    Event Operations Agent

    Responsibilities:
    - Agenda / Schedule Building
    - Conflict Detection & Resolution
    - Resource Planning (rooms, timing)
    - Capacity Validation
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ops_agent")

        self.config = config or {
            "start_time": "09:00",
            "end_time": "18:00",
            "slot_minutes": 60,
        }

    # ----------------------------------------
    # TIME SLOT GENERATION
    # ----------------------------------------

    def _generate_time_slots(self, num_days: int):
        slots = []
        fmt_time = "%H:%M"

        current_time = datetime.strptime(self.config["start_time"], fmt_time)
        end_time = datetime.strptime(self.config["end_time"], fmt_time)

        for day in range(num_days):
            t = current_time
            while t + timedelta(minutes=self.config["slot_minutes"]) <= end_time:
                slot_end = t + timedelta(minutes=self.config["slot_minutes"])

                slots.append(
                    {
                        "day": day + 1,
                        "start": t.strftime(fmt_time),
                        "end": slot_end.strftime(fmt_time),
                    }
                )
                t = slot_end

        return slots

    # ----------------------------------------
    # RESOURCE PLANNING
    # ----------------------------------------

    def _assign_rooms(self, venue, audience_size):
        # your venue schema → venues: List[Venue]
        main_venue = venue.venues[0] if venue.venues else None

        if not main_venue:
            return [{"name": "Main Hall", "capacity": audience_size}]

        return [
            {
                "name": main_venue.name,
                "capacity": main_venue.capacity,
            }
        ]

    # ----------------------------------------
    # SCHEDULE BUILDER
    # ----------------------------------------

    def _build_schedule(self, speakers, rooms):
        slots = self._generate_time_slots(num_days=1)
        schedule = []

        speaker_pool = speakers.copy()
        random.shuffle(speaker_pool)

        i = 0
        for slot in slots:
            for room in rooms:
                if i >= len(speaker_pool):
                    break

                speaker = speaker_pool[i]

                schedule.append(
                    {
                        "speaker": speaker.name,
                        "topic": speaker.suggested_topic,
                        "room": room["name"],
                        "room_capacity": room["capacity"],
                        "start": slot["start"],
                        "end": slot["end"],
                    }
                )

                i += 1

        return schedule

    # ----------------------------------------
    # CONFLICT DETECTION
    # ----------------------------------------

    def _detect_conflicts(self, schedule: List[Dict]):
        conflicts = []

        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                s1, s2 = schedule[i], schedule[j]

                if s1["speaker"] == s2["speaker"]:
                    if not (s1["end"] <= s2["start"] or s2["end"] <= s1["start"]):
                        conflicts.append(
                            {
                                "type": "speaker_overlap",
                                "speaker": s1["speaker"],
                            }
                        )

        return conflicts

    # ----------------------------------------
    # MAIN RUN
    # ----------------------------------------

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("OpsAgent started")

            # ---- READ DEPENDENCIES ----
            speaker_data: SpeakerAgentOutput = state["outputs"]["speaker_agent"]
            venue_data: VenueAgentOutput = state["outputs"]["venue_agent"]

            audience_size = state["input"]["audience_size"]

            speakers = speaker_data.speakers

            # ---- BUILD ----
            rooms = self._assign_rooms(venue_data, audience_size)
            schedule = self._build_schedule(speakers, rooms)

            conflicts = self._detect_conflicts(schedule)

            result = {
                "schedule": schedule,
                "rooms": rooms,
                "conflicts": conflicts,
            }

            logger.info("OpsAgent completed")

            return self._success(result)

        except Exception as e:
            logger.exception("OpsAgent failed")
            return self._fail(e)
