# What is API Versioning? Two Strategies for Designing Better APIs

**Reference:** [YouTube Video](https://www.youtube.com/watch?v=vsb4ZkUytrU)

---

## Overview

API versioning is a critical strategy for keeping APIs changing and improving without breaking existing clients. It enables teams to evolve their APIs while maintaining backward compatibility and ensuring a smooth experience for all consumers.

---

## Application Programming Interface (API)

### Definition
A set of rules that allow different software entities to communicate with each other. Proper API design ensures continuous improvement without disrupting existing clients.

### Key Principles

**Backward Compatibility**
- Continue to support existing clients
- Avoid breaking changes that force immediate upgrades
- Provide deprecation periods and migration paths

**Forward Compatibility**
- Challenge to think ahead of time
- Anticipate future needs and extensions
- Design flexible contracts

**Separation of Concerns**
- Publish separately from implementation
- Hide internal implementation details
- Focus on public contract stability

**Lifecycle Management**
- Mark version deprecations
- Provide clear migration paths
- Communicate timelines to API consumers
- API lifecycle management

---

## Semantic Versioning

### Format
`MAJOR.MINOR.PATCH`

### Components

**MAJOR Version**
- Incremented for incompatible changes
- Breaking changes to the API
- Requires client updates
- Example: `2.0.0` (significant redesign)

**MINOR Version**
- Incremented for backward compatible functionality additions
- New features that don't break existing code
- Clients can upgrade without code changes
- Example: `1.5.0` (new optional field added)

**PATCH Version**
- Incremented for backward compatible bug fixes
- Security patches and minor corrections
- Safe to upgrade automatically
- Example: `1.4.2` (bug fix in existing feature)

---

## Semantic Versioning Examples

| Version | Type | Description |
|---------|------|-------------|
| 1.0.0 → 2.0.0 | MAJOR | Database schema redesign, removed endpoints |
| 1.5.0 → 1.6.0 | MINOR | Added new optional query parameter |
| 1.5.0 → 1.5.1 | PATCH | Fixed calculation bug in response |
| 0.1.0 → 0.2.0 | MINOR | Pre-release development versions |

---

## API Versioning Strategies

### Strategy 1: URL Path Versioning
- Include version in the URI path
- Example: `/api/v1/users`, `/api/v2/users`
- **Pros**: Clear and explicit
- **Cons**: Requires maintaining multiple endpoints

### Strategy 2: Query Parameter Versioning
- Include version as a query parameter
- Example: `/api/users?version=1.0`
- **Pros**: Single endpoint, flexible versioning
- **Cons**: Less visible in logs and documentation

### Strategy 3: Header-Based Versioning
- Include version in HTTP headers
- Example: `Accept: application/vnd.myapp.v1+json`
- **Pros**: Clean URLs, semantically correct
- **Cons**: Less discoverable by API consumers

### Strategy 4: Custom Header Versioning
- Custom header specifies API version
- Example: `X-API-Version: 2.0`
- **Pros**: Flexible and explicit
- **Cons**: Requires client awareness

---

## Best Practices for API Versioning

1. **Plan Ahead**: Design versioning strategy before public release
2. **Clear Communication**: Document version timelines and deprecations
3. **Long Transition Periods**: Provide adequate time for clients to migrate
4. **Support Multiple Versions**: Maintain at least two supported versions
5. **Deprecation Notices**: Add deprecation headers and documentation
6. **Semantic Versioning**: Follow established conventions consistently
7. **Backward Compatibility**: Maintain compatibility where possible
8. **Version Lifecycle**: Define clear start and end of life for each version

---

## Version Lifecycle Example

```
Version 1.0 Released
   ↓ (6 months)
Version 2.0 Released (v1.0 still supported)
   ↓ (6 months)
Version 1.0 Deprecated (announcement + 6 month warning)
   ↓ (6 months)
Version 1.0 End of Life (sunset)
   ↓
Version 2.0 Only Supported
```

---

## Common Mistakes to Avoid

- ❌ Not versioning from the start
- ❌ Forcing immediate upgrades
- ❌ Poor documentation of breaking changes
- ❌ Supporting too many versions simultaneously
- ❌ Vague deprecation timelines
- ❌ Breaking backward compatibility in minor versions
- ❌ Inconsistent versioning schemes

