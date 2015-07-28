# Messages

## Event

The Event message results in the recording of an event against a version and run of an item (article)

### properties

- item-identifier - the f-id, e.g. 00288, 00013, derrived from the numeric portion of the DOI
- version - the version of the item the event was raised against
- run - the processing run attempt of the item the event was raised against
- type - the event type, these are the events displayed upon within the dashboard
- timestamp - a timestamp for the event
- status - start|end|error defines the status for this event type that this message represents
- message - text message to be displayed in the dashboard giving extra information

### example payloads

```json
{
	"message_type": "event"
	"item_identifier": "00288",
	"version": 2,
	"run": 1,
	"event_type": "Image resizing",
	"timestamp": "2015-05-23T18:25:43.511Z",
	"status": "start",
	"message": "",
	"message_id": "2507ba51-7c1b-11e2-8ee5-70cd60f2c980"
}
```
 
```json
{
	"message_type": "event"
	"item_identifier": "00288",
	"version": 2,
	"run": 1,
	"event_type": "EIF submission",
	"timestamp": "2015-05-19T10:25:33.345Z",
	"status": "error",
	"message": "Could not contact EIF ingestion endpoint"
	"message_id": "250938c7-7c1b-11e2-b456-70cd60f2c980"
}
```
## Property

The Propety message applies a property to an item (article)
The dashboard may display these properties and/or use them to choose an 'event map' with which to display the events that have occured to processing runs against versions of the item.

### properties

- item-identifier - the f-id, e.g. 00288, 00013, derrived from the numeric portion of the DOI
- name - the name of the property to set
- value - the value of the property to set
- property-type - int|date|text what type of property the value is

### example payloads

```json
{
	"message-type": "property"
	"item_identifier": "00288",
	"name": "Title",
	"value": "Rapid localized spread and immunologic containment define Herpes simplex virus-2 reactivation in the human genital tract",
	"property_type": "text"
	"message-id": "2500b32e-7c1b-11e2-830a-70cd60f2c980"
}
```

```json
{
	"message_type": "property"
	"item-identifier": "00288",
	"name": "Corresponding authors",
	"value": "Ian T Baldwin, Max Planck, John Anderson, Thomas Peel",
	"property_type": "text"
	"message-id": "25093ae3-7c1b-11e2-940c-70cd60f2c980"
}
```