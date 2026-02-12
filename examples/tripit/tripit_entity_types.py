"""
TripIt Pydantic Entity and Edge Type Definitions for Graphiti

These models define entity types (node categories) and edge types (relationship categories)
derived from the TripIt API v1 data model (https://tripit.github.io/api/doc/v1). They are
designed to be passed to Graphiti's add_episode() or add_episode_bulk() methods at
configuration/initialization time.

Entity types guide the LLM in classifying extracted entities. Edge types and the edge type
map constrain and classify the relationships the LLM extracts between entities.

Usage:
    from tripit_entity_types import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP

    await graphiti.add_episode(
        name='itinerary_update',
        episode_body=episode_content,
        source_description='TripIt itinerary data',
        reference_time=datetime.now(timezone.utc),
        group_id='user_trips',
        entity_types=ENTITY_TYPES,
        edge_types=EDGE_TYPES,
        edge_type_map=EDGE_TYPE_MAP,
    )
"""

from pydantic import BaseModel, Field

# =============================================================================
# Entity Types (Node Categories)
# =============================================================================

# -- Travel Reservations ------------------------------------------------------


class Trip(BaseModel):
    """A planned trip or journey, serving as the top-level container for all travel
    reservations, activities, and notes. A trip has a destination, date range, and
    groups together flights, lodging, car rentals, and other travel objects."""

    start_date: str | None = Field(None, description='Trip start date (YYYY-MM-DD)')
    end_date: str | None = Field(None, description='Trip end date (YYYY-MM-DD)')
    destination: str | None = Field(None, description='Primary destination city or region')
    is_private: bool | None = Field(None, description='Whether the trip is private')


class Flight(BaseModel):
    """A flight reservation or individual flight segment. Represents air travel between
    two airports, including marketing/operating airline, flight number, and cabin class."""

    airline_code: str | None = Field(None, description='IATA airline code (e.g., "UA", "DL")')
    flight_number: str | None = Field(None, description='Flight number (e.g., "1234")')
    departure_airport: str | None = Field(
        None, description='Departure airport IATA code (e.g., "SFO")'
    )
    arrival_airport: str | None = Field(None, description='Arrival airport IATA code (e.g., "JFK")')
    departure_time: str | None = Field(None, description='Scheduled departure date and time')
    arrival_time: str | None = Field(None, description='Scheduled arrival date and time')
    service_class: str | None = Field(
        None, description='Class of service (e.g., "economy", "business", "first")'
    )
    aircraft_type: str | None = Field(None, description='Aircraft type (e.g., "Boeing 737-800")')
    seat_assignment: str | None = Field(None, description='Seat assignment (e.g., "12A")')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')
    record_locator: str | None = Field(None, description='PNR record locator')


class Lodging(BaseModel):
    """A hotel, resort, vacation rental, or other accommodation booking. Represents
    a stay at a lodging property with check-in/check-out dates and room details."""

    check_in_date: str | None = Field(None, description='Check-in date')
    check_out_date: str | None = Field(None, description='Check-out date')
    room_type: str | None = Field(None, description='Room type (e.g., "King Suite")')
    number_of_rooms: str | None = Field(None, description='Number of rooms booked')
    number_of_guests: str | None = Field(None, description='Number of guests')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')


class CarRental(BaseModel):
    """A car rental reservation. Represents a vehicle rental with pickup and
    dropoff locations, dates, and vehicle details."""

    pickup_date: str | None = Field(None, description='Pickup date and time')
    dropoff_date: str | None = Field(None, description='Dropoff date and time')
    car_type: str | None = Field(
        None, description='Vehicle category (e.g., "compact", "SUV", "luxury")'
    )
    car_description: str | None = Field(None, description='Vehicle description')
    pickup_location: str | None = Field(None, description='Pickup location name')
    dropoff_location: str | None = Field(None, description='Dropoff location name')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')


class RailJourney(BaseModel):
    """A rail or train reservation. Represents train travel between stations,
    including carrier, train number, and service class."""

    carrier: str | None = Field(None, description='Rail carrier name (e.g., "Amtrak", "Eurostar")')
    train_number: str | None = Field(None, description='Train number')
    departure_station: str | None = Field(None, description='Departure station name')
    arrival_station: str | None = Field(None, description='Arrival station name')
    departure_time: str | None = Field(None, description='Departure date and time')
    arrival_time: str | None = Field(None, description='Arrival date and time')
    service_class: str | None = Field(None, description='Class of service')
    seat_assignment: str | None = Field(None, description='Seat or coach assignment')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')


class Cruise(BaseModel):
    """A cruise reservation. Represents a cruise voyage with ship, cabin, and
    port of call information."""

    ship_name: str | None = Field(None, description='Name of the cruise ship')
    cabin_number: str | None = Field(None, description='Cabin number')
    cabin_type: str | None = Field(
        None, description='Cabin type (e.g., "interior", "balcony", "suite")'
    )
    departure_date: str | None = Field(None, description='Embarkation date')
    return_date: str | None = Field(None, description='Disembarkation date')
    departure_port: str | None = Field(None, description='Port of embarkation')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')


class GroundTransport(BaseModel):
    """Ground transportation such as a shuttle, limousine, bus, taxi, or ride service.
    Represents non-flight, non-rail transport between locations."""

    transport_type: str | None = Field(
        None, description='Type of transport (e.g., "shuttle", "limousine", "bus", "taxi")'
    )
    carrier: str | None = Field(None, description='Transport provider name')
    pickup_location: str | None = Field(None, description='Pickup location')
    dropoff_location: str | None = Field(None, description='Dropoff location')
    pickup_time: str | None = Field(None, description='Pickup date and time')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')


class Restaurant(BaseModel):
    """A restaurant reservation. Represents a dining reservation at a specific
    restaurant with time, party size, and cuisine details."""

    cuisine: str | None = Field(None, description='Type of cuisine')
    reservation_time: str | None = Field(None, description='Reservation date and time')
    party_size: str | None = Field(None, description='Number of diners')
    price_range: str | None = Field(None, description='Price range indicator')
    dress_code: str | None = Field(None, description='Dress code if applicable')
    confirmation_number: str | None = Field(None, description='Reservation confirmation number')


class Activity(BaseModel):
    """A planned activity, tour, excursion, or event during a trip. Represents
    things like museum visits, guided tours, shows, or sporting events."""

    activity_type: str | None = Field(
        None, description='Type of activity (e.g., "tour", "museum", "show", "excursion")'
    )
    start_time: str | None = Field(None, description='Activity start date and time')
    end_time: str | None = Field(None, description='Activity end date and time')
    venue: str | None = Field(None, description='Venue or location name')
    confirmation_number: str | None = Field(None, description='Booking confirmation number')


# -- People -------------------------------------------------------------------


class Traveler(BaseModel):
    """A person who is traveling or associated with travel reservations. May be a
    passenger on a flight, a guest at a hotel, a driver on a car rental, or a
    participant in an activity."""

    first_name: str | None = Field(None, description='First name')
    last_name: str | None = Field(None, description='Last name')
    email: str | None = Field(None, description='Email address')
    frequent_traveler_number: str | None = Field(
        None, description='Loyalty or frequent traveler program number'
    )
    meal_preference: str | None = Field(None, description='Meal preference for flights')
    seat_preference: str | None = Field(
        None, description='Seat preference (e.g., "window", "aisle")'
    )


# -- Locations ----------------------------------------------------------------


class Airport(BaseModel):
    """An airport. Identified by its IATA code and associated with a city."""

    iata_code: str | None = Field(None, description='IATA airport code (e.g., "SFO", "LHR")')
    city: str | None = Field(None, description='City the airport serves')
    country: str | None = Field(None, description='Country code')
    latitude: float | None = Field(None, description='Airport latitude')
    longitude: float | None = Field(None, description='Airport longitude')


class City(BaseModel):
    """A city or metropolitan area, typically a travel destination or origin."""

    country: str | None = Field(None, description='Country the city is in')
    state_or_region: str | None = Field(None, description='State, province, or region')
    timezone: str | None = Field(None, description='IANA timezone (e.g., "America/New_York")')


class Venue(BaseModel):
    """A specific named place such as a hotel property, restaurant, museum, train
    station, cruise port, or other point of interest."""

    venue_type: str | None = Field(
        None,
        description=(
            'Type of venue (e.g., "hotel", "restaurant", "museum", "train_station", "cruise_port")'
        ),
    )
    address: str | None = Field(None, description='Street address')
    phone: str | None = Field(None, description='Phone number')
    url: str | None = Field(None, description='Website URL')
    latitude: float | None = Field(None, description='Venue latitude')
    longitude: float | None = Field(None, description='Venue longitude')


# -- Organizations ------------------------------------------------------------


class Airline(BaseModel):
    """An airline company that operates or markets flights."""

    iata_code: str | None = Field(None, description='IATA airline code (e.g., "UA", "BA")')
    alliance: str | None = Field(
        None, description='Airline alliance (e.g., "Star Alliance", "oneworld")'
    )


class TransportProvider(BaseModel):
    """A company that provides transportation services such as car rentals,
    rail service, cruise lines, shuttle services, or ride-hailing."""

    provider_type: str | None = Field(
        None,
        description=(
            'Type of provider (e.g., "car_rental", "rail", "cruise_line", '
            '"shuttle", "ride_service")'
        ),
    )
    phone: str | None = Field(None, description='Contact phone number')
    url: str | None = Field(None, description='Website URL')


class LoyaltyProgram(BaseModel):
    """A frequent traveler loyalty or points program, such as airline miles
    programs, hotel rewards, or rental car loyalty programs."""

    program_type: str | None = Field(
        None,
        description='Type of program (e.g., "airline_miles", "hotel_points", "car_rental")',
    )
    balance: str | None = Field(None, description='Current points or miles balance')
    elite_status: str | None = Field(
        None, description='Elite tier status (e.g., "Gold", "Platinum")'
    )


# =============================================================================
# Edge Types (Relationship Categories)
# =============================================================================


class PartOfTrip(BaseModel):
    """A reservation, activity, or note belongs to a specific trip. This is the
    primary containment relationship linking travel objects to their parent trip."""


class DepartsFrom(BaseModel):
    """A flight, rail journey, cruise, or ground transport departs from a
    specific airport, station, port, or location."""

    scheduled_time: str | None = Field(None, description='Scheduled departure date and time')
    terminal: str | None = Field(None, description='Terminal or platform')
    gate: str | None = Field(None, description='Gate number')


class ArrivesAt(BaseModel):
    """A flight, rail journey, cruise, or ground transport arrives at a
    specific airport, station, port, or location."""

    scheduled_time: str | None = Field(None, description='Scheduled arrival date and time')
    terminal: str | None = Field(None, description='Terminal or platform')
    gate: str | None = Field(None, description='Gate number')
    baggage_claim: str | None = Field(None, description='Baggage claim area')


class LocatedAt(BaseModel):
    """A lodging, restaurant, activity, or other place-bound entity is
    physically located at a specific venue or address."""


class LocatedIn(BaseModel):
    """An airport, venue, or other location is situated within a city or region."""


class OperatedBy(BaseModel):
    """A flight is operated by an airline, or a transport/rental/cruise is
    provided by a transport provider."""

    operating_code: str | None = Field(
        None, description='Operating carrier code if different from marketing carrier'
    )


class BookedWith(BaseModel):
    """A reservation was booked through a specific booking site, travel agent,
    or provider."""

    booking_site: str | None = Field(None, description='Name of the booking site or agency')
    booking_reference: str | None = Field(None, description='Booking site confirmation number')
    booking_date: str | None = Field(None, description='Date the booking was made')
    total_cost: str | None = Field(None, description='Total cost of the booking')


class TravelerOn(BaseModel):
    """A traveler is a passenger, guest, driver, or participant on a reservation.
    The role varies by reservation type (passenger for flights, guest for hotels,
    driver for car rentals, participant for activities)."""

    role: str | None = Field(
        None,
        description=(
            'Role of the traveler (e.g., "passenger", "guest", "driver", '
            '"participant", "reservation_holder")'
        ),
    )
    ticket_number: str | None = Field(None, description='Ticket number if applicable')


class ConnectsTo(BaseModel):
    """A flight segment, rail segment, or transport segment connects to a
    subsequent segment, forming a multi-leg itinerary."""

    connection_time: str | None = Field(
        None, description='Layover or connection time between segments'
    )
    connection_airport: str | None = Field(None, description='Connection airport or station code')


class MemberOf(BaseModel):
    """A traveler is a member of a loyalty or frequent traveler program."""

    member_number: str | None = Field(None, description='Membership or account number')
    elite_status: str | None = Field(None, description='Elite tier status')


class OfferedBy(BaseModel):
    """A loyalty program is offered by an airline or transport provider."""


class DestinationOf(BaseModel):
    """A city or location is the destination (or origin) of a trip."""

    role: str | None = Field(
        None, description='Whether this is an "origin" or "destination" of the trip'
    )


class PortOfCall(BaseModel):
    """A cruise stops at a specific port city as part of its itinerary."""

    arrival_date: str | None = Field(None, description='Arrival date at port')
    departure_date: str | None = Field(None, description='Departure date from port')


class InvitedTo(BaseModel):
    """A traveler has been invited to or is sharing a trip with another traveler."""

    is_read_only: bool | None = Field(None, description='Whether the invitee has read-only access')
    is_traveler: bool | None = Field(
        None, description='Whether the invitee is also traveling on this trip'
    )


# =============================================================================
# Configuration Dictionaries
# =============================================================================

ENTITY_TYPES: dict[str, type[BaseModel]] = {
    # Travel reservations
    'Trip': Trip,
    'Flight': Flight,
    'Lodging': Lodging,
    'CarRental': CarRental,
    'RailJourney': RailJourney,
    'Cruise': Cruise,
    'GroundTransport': GroundTransport,
    'Restaurant': Restaurant,
    'Activity': Activity,
    # People
    'Traveler': Traveler,
    # Locations
    'Airport': Airport,
    'City': City,
    'Venue': Venue,
    # Organizations
    'Airline': Airline,
    'TransportProvider': TransportProvider,
    'LoyaltyProgram': LoyaltyProgram,
}

EDGE_TYPES: dict[str, type[BaseModel]] = {
    'PART_OF_TRIP': PartOfTrip,
    'DEPARTS_FROM': DepartsFrom,
    'ARRIVES_AT': ArrivesAt,
    'LOCATED_AT': LocatedAt,
    'LOCATED_IN': LocatedIn,
    'OPERATED_BY': OperatedBy,
    'BOOKED_WITH': BookedWith,
    'TRAVELER_ON': TravelerOn,
    'CONNECTS_TO': ConnectsTo,
    'MEMBER_OF': MemberOf,
    'OFFERED_BY': OfferedBy,
    'DESTINATION_OF': DestinationOf,
    'PORT_OF_CALL': PortOfCall,
    'INVITED_TO': InvitedTo,
}

EDGE_TYPE_MAP: dict[tuple[str, str], list[str]] = {
    # -- Trip containment: reservations belong to trips --
    ('Flight', 'Trip'): ['PART_OF_TRIP'],
    ('Lodging', 'Trip'): ['PART_OF_TRIP'],
    ('CarRental', 'Trip'): ['PART_OF_TRIP'],
    ('RailJourney', 'Trip'): ['PART_OF_TRIP'],
    ('Cruise', 'Trip'): ['PART_OF_TRIP'],
    ('GroundTransport', 'Trip'): ['PART_OF_TRIP'],
    ('Restaurant', 'Trip'): ['PART_OF_TRIP'],
    ('Activity', 'Trip'): ['PART_OF_TRIP'],
    # -- Departure / arrival for transport types --
    ('Flight', 'Airport'): ['DEPARTS_FROM', 'ARRIVES_AT'],
    ('RailJourney', 'Venue'): ['DEPARTS_FROM', 'ARRIVES_AT'],
    ('Cruise', 'Venue'): ['DEPARTS_FROM', 'ARRIVES_AT', 'PORT_OF_CALL'],
    ('GroundTransport', 'Venue'): ['DEPARTS_FROM', 'ARRIVES_AT'],
    ('CarRental', 'Venue'): ['DEPARTS_FROM', 'ARRIVES_AT'],
    # -- Physical location --
    ('Lodging', 'Venue'): ['LOCATED_AT'],
    ('Restaurant', 'Venue'): ['LOCATED_AT'],
    ('Activity', 'Venue'): ['LOCATED_AT'],
    # -- Geographic containment --
    ('Airport', 'City'): ['LOCATED_IN'],
    ('Venue', 'City'): ['LOCATED_IN'],
    # -- Trip destinations --
    ('Trip', 'City'): ['DESTINATION_OF'],
    # -- Cruise port of call --
    ('Cruise', 'City'): ['PORT_OF_CALL'],
    # -- Operators / providers --
    ('Flight', 'Airline'): ['OPERATED_BY'],
    ('RailJourney', 'TransportProvider'): ['OPERATED_BY'],
    ('Cruise', 'TransportProvider'): ['OPERATED_BY'],
    ('GroundTransport', 'TransportProvider'): ['OPERATED_BY'],
    ('CarRental', 'TransportProvider'): ['OPERATED_BY'],
    # -- Booking provenance --
    ('Flight', 'Entity'): ['BOOKED_WITH'],
    ('Lodging', 'Entity'): ['BOOKED_WITH'],
    ('CarRental', 'Entity'): ['BOOKED_WITH'],
    ('RailJourney', 'Entity'): ['BOOKED_WITH'],
    ('Cruise', 'Entity'): ['BOOKED_WITH'],
    ('GroundTransport', 'Entity'): ['BOOKED_WITH'],
    ('Restaurant', 'Entity'): ['BOOKED_WITH'],
    ('Activity', 'Entity'): ['BOOKED_WITH'],
    # -- Traveler associations --
    ('Traveler', 'Flight'): ['TRAVELER_ON'],
    ('Traveler', 'Lodging'): ['TRAVELER_ON'],
    ('Traveler', 'CarRental'): ['TRAVELER_ON'],
    ('Traveler', 'RailJourney'): ['TRAVELER_ON'],
    ('Traveler', 'Cruise'): ['TRAVELER_ON'],
    ('Traveler', 'GroundTransport'): ['TRAVELER_ON'],
    ('Traveler', 'Restaurant'): ['TRAVELER_ON'],
    ('Traveler', 'Activity'): ['TRAVELER_ON'],
    ('Traveler', 'Trip'): ['INVITED_TO'],
    # -- Multi-segment connections --
    ('Flight', 'Flight'): ['CONNECTS_TO'],
    ('RailJourney', 'RailJourney'): ['CONNECTS_TO'],
    ('GroundTransport', 'GroundTransport'): ['CONNECTS_TO'],
    # -- Loyalty programs --
    ('Traveler', 'LoyaltyProgram'): ['MEMBER_OF'],
    ('LoyaltyProgram', 'Airline'): ['OFFERED_BY'],
    ('LoyaltyProgram', 'TransportProvider'): ['OFFERED_BY'],
}
