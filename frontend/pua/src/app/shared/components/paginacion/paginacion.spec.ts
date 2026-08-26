import { describe, it, expect, beforeEach } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ɵresolveComponentResources as resolveComponentResources } from '@angular/core';
import { PaginacionComponent } from './paginacion';

describe('PaginacionComponent', () => {
  let component: PaginacionComponent;
  let fixture: ComponentFixture<PaginacionComponent>;

  beforeEach(async () => {
    await resolveComponentResources(() => Promise.resolve('<div></div>'));
    await TestBed.configureTestingModule({
      imports: [PaginacionComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PaginacionComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
