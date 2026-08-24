import { TestBed } from '@angular/core/testing';

import { Agresores } from './agresores';

describe('Agresores', () => {
  let service: Agresores;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Agresores);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
