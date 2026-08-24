import { TestBed } from '@angular/core/testing';

import { BaseCrud } from './base-crud';

describe('BaseCrud', () => {
  let service: BaseCrud;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BaseCrud);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
